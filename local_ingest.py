import os
import pandas as pd
import numpy as np
import pyarrow
from sqlalchemy import create_engine
import time

def main():

    # Declare the ingestion script parameters
    user="osboxes"
    password="osboxes.org"
    host="localhost"
    port=5432
    db="ny_taxi"
    table_name="ny_taxi"
    url = r'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet'
    parquet_name = 'yellow_tripdata_2022-01.parquet'

    # Download parquet file from the url
    #df = os.system(f"wget {url} -O {parquet_name}")
    #df = pd.read_parquet(url, engine='pyarrow')
    df = pd.read_parquet(parquet_name, engine='pyarrow')

    # Connect to Postgres with SQLAlchemy
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Convert datetime fields to pandas datetime types
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Convert Schema to DDL with SQLAlchemy
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Insert data into postgres database by chunks
    df_iter = pd.read_parquet(parquet_name, iterator=True, chunksize=10000)
    #df = next(df_iter)

    # Insert dataframe values in Postgres Database
    #df.to_sql(name=table_name, con=engine, if_exists='append')

    # Time the ingestion process and print ingestion status
    while True:
        try:
            t_start = time()

            df = next(df_iter)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, it took %.3f seconds' % (t_end - t_start))

        except:
            print("That was the last chunk to ingest")
        
        else:
            print("Next chunk loading...")
    
    print("Completed data ingestion to PostgreSQL")

if '__name__' == '__main__':
    main()