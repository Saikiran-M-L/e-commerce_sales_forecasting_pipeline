import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def ingest_data():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ecommerce"]
    raw_col = db["raw_data"]
    local_path = "data/Ecommerce.csv"
    df = pd.read_csv(local_path)

    records = df.to_dict(orient="records")
    raw_col.delete_many({})
    raw_col.insert_many(records)
    print(f"Inserted {len(records)} rows into raw_data")


if __name__ == "__main__":
    ingest_data()
