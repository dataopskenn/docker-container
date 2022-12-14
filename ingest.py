import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import time


def main(params):

    # Declare the ingestion script parameters
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params,table_name
    url = params.url
    parquet_name = 'output.parquet'

    # Download parquet file from the url
    os.system(f"wget {url} -O {parquet_name}")

    # Connect to Postgres with SQLAlchemy
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Convert datetime fields to pandas datetime types
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Convert Schema to DDL with SQLAlchemy
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # Insert data into ostgres database by chunks
    df_iter = pd.read_parquet(parquet_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    # Insert dataframe values in Postgres Database
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Time the ingestion process and print ingestion status
    while True:
        try:
            t_start = time()

            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, it took %.3f seconds' % (t_end - t_start))

        except:
            print("That was the last chunk to ingest")
        
        else:
            print("Completed data ingestion to PostgreSQL")

if '__name__' == '__main__':
    main()