import pandas as pd
from database.access import SDA
from seoul_moving.clean import long_foreigner, short_foreigner, locals
from datetime import datetime


def insert_foreign_long_history(db: SDA, path, start_date, end_date):
    batch_size = 50000

    for dt in pd.date_range(start_date, end_date):
        data = long_foreigner(path, datetime(dt.year, dt.month, dt.day)) 

        # Insert data in batches
        for i in range(0, data.shape[0], batch_size):
            try:
                batch = data.iloc[i:i+batch_size]
                db.insert_dataframe(batch, "longterm_foreign", "nimbus")
            except Exception as e:
                print("[IMPORTANT] Error inserting data >>>", e)
                print("[IMPORTANT] Restart from date >>>", dt)
                raise e

        print(dt, "done")


def insert_foreign_short_history(db: SDA, path, start_date, end_date):
    batch_size = 50000

    for dt in pd.date_range(start_date, end_date):
        data = short_foreigner(path, datetime(dt.year, dt.month, dt.day)) 

        # Insert data in batches
        for i in range(0, data.shape[0], batch_size):
            try:
                batch = data.iloc[i:i+batch_size]
                db.insert_dataframe(batch, "shortterm_foreign", "nimbus")
            except Exception as e:
                print("[IMPORTANT] Error inserting data >>>", e)
                print("[IMPORTANT] Restart from date >>>", dt)
                raise e

        print(dt, "done")


def insert_local_history(db: SDA, path, start_date, end_date):
    batch_size = 50000

    for dt in pd.date_range(start_date, end_date):
        data = locals(path, datetime(dt.year, dt.month, dt.day))    

        # Insert data in batches
        for i in range(0, data.shape[0], batch_size):
            try:
                batch = data.iloc[i:i+batch_size]
                db.insert_dataframe(batch, "locals", "nimbus")
            except Exception as e:
                print("[IMPORTANT] Error inserting data >>>", e)
                print("[IMPORTANT] Restart from date >>>", dt)
                raise e

        print(dt, "done")
