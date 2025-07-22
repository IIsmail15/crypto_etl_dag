#imporing Airflow's core library for defining a DAG 
from airflow import DAG

#importing Python-Operator- think of Operators as the'tools' that will help run your python function/task
from airflow.operators.python import PythonOperator

#Datetime: to handle dates and times ( important for scheduling)
from datetime import datetime 

#Requests is a Python Library to call external API (we'll use it to fetch the crypto data)
import requests 

#pandas helps us work with tabluar data 
import pandas as pd

#The os module helps us work with file paths and directories
import os 
## JSON module helps read and write JSON data (which is how the API will return data) 
import json

#to connect to the Database 
from sqlalchemy import create_engine 




# This is the folder inside the Airflow container where our output files will be stored
OUTPUT_DIR = "/opt/airflow/data"

# This is the full path to the raw data file — we’re using an f-string to combine the folder and file name
RAW_DATA_PATH = f"{OUTPUT_DIR}/raw_crypto.json"

# This is where our cleaned and transformed CSV file will be saved
TRANSFORMED_PATH = f"{OUTPUT_DIR}/crypto_prices.csv"


def extract(): 
    #this is the API endpoint we'll use to get crypto.Currency makret data 
    url= "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",  # We want prices in USD
        "order": "market_cap_desc", # Sort by market cap (biggest coins first)
        "per_page":10,  # Only get the top 5 coins
        "page":1,     # First page of results
        "sparkline": False # We don’t need historical mini-charts
    }
    #we make a GET request to the API using the URL and params you wrote above.  
    response = requests.get(url ,params=params)
    # response.json convert the response into json and save it into the variable data 
    data=response.json() 

    #Create the output folder if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # save the raw JSON response to a file
    with open (RAW_DATA_PATH, "w") as f: 
        json.dump(data,f)  
 





def transform(): 
    with open(RAW_DATA_PATH, "r") as f:
        data = json.load(f) # here we are opening the folder/file with most write to make amendment

    df = pd.DataFrame(data)[["id", "symbol", "current_price","market_cap", "last_updated" ]] #we transform the json data to a dataframe with following ID's
    df.to_csv(TRANSFORMED_PATH, index=False) #save it to a different path


def load(): 

    # 1. Read the transformed CSV
    df = pd.read_csv(TRANSFORMED_PATH)

    # 2. Set up database connection (credentials from .env)
    user ="airflow"
    password = "airflow"
    host = "postgres"
    port= "5432"
    db= "crypto_data"

    engine= create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

   # 3. Write to PostgreSQL
    df.to_sql("coins", engine, if_exists="replace", index=False)

    print("Data written to postgres table: crypto_prices")





default_args = {
    "start_date": datetime(2023,1,1)
}

with DAG(
    dag_id="crypto_etl_pipeline_etl_steps",        # Unique name for your DAG
    schedule_interval="@daily",                    # Run this DAG once per day
    default_args=default_args,                     # Apply default settings (like start date)
    catchup=False,                                 # Don’t backfill old runs
    tags=["crypto", "etl", "structured"]           # For filtering in the UI
) as dag:

    extract_task = PythonOperator(
        task_id="extract_crypto_data",
        python_callable=extract                   # Calls the extract() function
    )

    transform_task = PythonOperator(
        task_id="transform_crypto_data",
        python_callable=transform                 # Calls the transform() function
    )

    load_task = PythonOperator(
        task_id="load_crypto_data",
        python_callable=load                      # Calls the load() function
    )

    # Define task execution order: Extract >> Transform >> Load
    extract_task >> transform_task >> load_task
