import datetime as dt
from datetime import timedelta, date
import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()

default_args = {
    'depends_on_past': False,
    'owner'     : 'airflow',
    'start_date': dt.datetime.now(),
    'retries'   : '1',
    'retry_delay' : dt.timedelta(minutes=5)
}

def queryPostgresql():
    con = "dbname = 'postgres' host='192.168.1.48' user='postgres' password=''"
    d = date.today()
    t = dt.timedelta(days=1)
    a = d - t
    try:
        connection = db.connect(con)
    except:
        print("Error Connecting to Postgres Database")
    try:
        df=pd.read_sql(f"select * from seeclickfix where date = '{a}'",connection)
    except:
        print("Error querying data from postgres OR pandas related Error")
    df.to_csv('postgredata.csv')
    print("------Data Received Successfully from Postgres------")

def insertElasticsearch():    
    es = Elasticsearch(
        ['https://192.168.1.41:9200'],
        http_auth=('elastic', ''),
        verify_certs=False
    )
    df=pd.read_csv('postgredata.csv')
    for i,r in df.iterrows():
        doc = r.to_json()
        print(doc)
        res = es.index(index="scf",id=r['id'],body=doc)
        print(res)
    print("----Data Saved to Elastic!----")
    os.remove('postgredata.csv')

with DAG(
    'postgre_to_elastic_seeClickFix', #this is DAG ID
    default_args=default_args,
    description="CVS to JSON Simple Pipeline",
    schedule_interval=timedelta(hours=24)
) as dag:
    getData = PythonOperator(task_id='QueryPostgreSQL',
        python_callable=queryPostgresql)
    
    insertData = PythonOperator(task_id='InsertToElasticsearch',
        python_callable=insertElasticsearch)

getData >> insertData