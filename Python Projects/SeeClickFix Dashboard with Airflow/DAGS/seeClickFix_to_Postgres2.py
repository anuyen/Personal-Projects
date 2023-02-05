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

import urllib3
urllib3.disable_warnings()

default_args = {
    'depends_on_past': False,
    'owner'     : 'airflow',
    'start_date': dt.datetime.now(),
    'retries'   : '1',
    'retry_delay' : dt.timedelta(minutes=5)
}

def fetchData():
    url = 'https://seeclickfix.com/api/v2/issues?place_url=santa-clara-county'
    try:
        r = requests.get(url).content
    except:
        print("Trouble fetch http request from seeclickfix")
    data = json.loads(r.decode('utf-8'))
    df = pd.DataFrame(data['issues']).reset_index()
    df.to_csv('issues.csv')

def transformDate():
    try:
        data = pd.read_csv('issues.csv')
    except IOError:
        print("Trouble opening file")
    date = data['created_at'].str.split(pat='T',n=1,expand=True)
    data['date']=date[0]
    use_df = data[['id','summary','description','rating','lat','lng','address','date']]
    use_df.to_csv('filtered.csv')
    os.remove('issues.csv')

def inputToPostgres():
    try:
        con = "dbname = 'postgres' host='192.168.1.41' user='postgres' password=''"
        connection = db.connect(con)
        cur=connection.cursor()
    except:
        print("Trouble connecting to postgres server")
    try:
        df = pd.read_csv('filtered.csv')
    except IOError:
        print("Trouble opening file")
    cur.execute(query='create table if not exists seeClickFix(id bigint primary key, summary text, description text, rating int, lat double precision, long double precision, address text, date date)')
    for i,r in df.iterrows():
        id = r['id']
        summary = r['summary']
        desc = str(r['description'])
        desc = desc.replace('\'','')
        rat = r['rating']
        lat = r['lat']
        lng = r['lng']
        add = str(r['address'])
        add = add.replace('\'','')
        dat = r['date']
        try: 
            cur.execute(query=f"insert into seeClickFix(id, summary, description, rating, lat, long, address, date) values({id},'{summary}','{desc}',{rat},{lat},{lng},'{add}','{dat}');")
        except:
            print("something is wrong with inserting this data. Probably duplicates")
    connection.commit()
    cur.close()
    connection.close()
    os.remove('filtered.csv')

with DAG(
    'seeClickFix_to_postgres2', #this is DAG ID
    default_args=default_args,
    description="Input relevant date from seeClickFix in the Santa Clara region and input it into postgredb",
    schedule_interval=timedelta(hours=8)
) as dag:
    getData = PythonOperator(task_id='getData',
        python_callable=fetchData)
    
    filter = PythonOperator(task_id='filterData',
        python_callable=transformDate)

    insertData = PythonOperator(task_id='InsertToPostgres',
        python_callable=inputToPostgres)

getData >> filter >> insertData