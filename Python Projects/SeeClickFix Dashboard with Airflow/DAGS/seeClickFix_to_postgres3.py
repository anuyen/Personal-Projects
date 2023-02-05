import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import psycopg2 as db
import requests
import os
import json
import pygeohash as gh

import urllib3
urllib3.disable_warnings()

default_args = {
    'depends_on_past': False,
    'owner'     : 'airflow',
    'start_date': '2022-11-19 18:56:48.011580',
    'retries'   : '1',
    'retry_delay' : dt.timedelta(minutes=5)
}

def printTime():
    print(dt.datetime.now())

def fetchData():
    url = 'https://seeclickfix.com/api/v2/issues?place_url=santa-clara-county'
    try:
        r = requests.get(url).content
    except:
        print("Trouble fetch http request from seeclickfix")
    data = json.loads(r.decode('utf-8'))
    df = pd.DataFrame(data['issues']).reset_index()
    print(df.head(2))
    df.to_csv('issues.csv')

def transformData():
    try:
        df = pd.read_csv('issues.csv')
    except IOError:
        print("Trouble opening file")

    #splitting datetime into date and time
    print("Starting datetime split...")
    datetime = df['created_at'].str.split(pat='T',n=1,expand=True)
    date = datetime[0]
    time = datetime[1].str.split(pat='-',expand=True,n=1)
    time = time[0]
    df['date']=date[0]
    df['time']=time[0]
    print(df.head(2))

    #rename address into full_address
    print("Renaming address column to full_address...")
    df = df.rename(columns={'address':'full_address'})
    print(df.head(2))

    #extract zipcode
    print("Extracting zip code")
    street = df['full_address']
    df['zip_code'] = street.str.extract(r'(9\d{4})')
    df['zip_code'].fillna(value=00000,inplace=True)
    print(df.head(2))

    #convert long,lat into geopoints
    print("Converting lat long into geopoints")
    longlat = df[['lat','lng']]
    longlat['geohash']=longlat.apply(lambda x: gh.encode(x.lat, x.lng, precision=10), axis=1)
    df['coordinate']=longlat['geohash']
    print(df.head(2))

    #extract columns we care about
    print("Collecting final dataframe")
    our_df = df[['id','summary','description','rating','full_address','html_url','date','time','zip_code','coordinate']]
    our_df.head(5)

    #saving to .csv file
    print("Saving to .csv")
    our_df.to_csv('filtered.csv')
    print("Removing source file")
    os.remove('issues.csv')

def inputToPostgres():
    try:
        con = "dbname = 'postgres' host='192.168.1.48' user='postgres' password=''"
        connection = db.connect(con)
        cur=connection.cursor()
    except:
        print("Trouble connecting to postgres server")
    try:
        df = pd.read_csv('filtered.csv')
    except IOError:
        print("Trouble opening file")
    
    #insert into table
    for i,r in df.iterrows():
        id = r['id']
        summary = r['summary']
        summary = summary.replace('\'','')
        desc = str(r['description'])
        desc = desc.replace('\'','')
        rating = r['rating']
        f_add = str(r['full_address'])
        f_add = f_add.replace('\'','')
        url = r['html_url']
        dat = r['date']
        zip = r['zip_code']
        coord = r['coordinate']

        insert = "insert into scf(id, summary, description, rating, full_address, date, html_url, zipcode, coordinate) "
        try: 
            cur.execute(query=insert + f"values({id},'{summary}','{desc}',{rating},'{f_add}','{dat}','{url}',{zip},'{coord}');")
        except:
            print("something is wrong with inserting this data. Probably duplicates")

    #commit
    connection.commit()
    cur.close()
    connection.close()
    os.remove('filtered.csv')

with DAG(
    'seeClickFix_to_postgres3', #this is DAG ID
    default_args=default_args,
    description="Input relevant date from seeClickFix in the Santa Clara region and input it into postgredb",
    schedule_interval=timedelta(hours=8)
) as dag:
    logTime = PythonOperator(task_id='logTime', python_callable=printTime)

    getData = PythonOperator(task_id='getData',
        python_callable=fetchData)
    
    filter = PythonOperator(task_id='filterData',
        python_callable=transformData)

    insertData = PythonOperator(task_id='InsertToPostgres',
        python_callable=inputToPostgres)

logTime >> getData >> filter >> insertData