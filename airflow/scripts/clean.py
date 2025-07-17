import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def clean_data():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ecommerce"]

    df = pd.DataFrame(list(db["raw_data"].find()))
    df = df.dropna()
    df["Quantity"] = df["Quantity"].abs()
    df = df[df["UnitPrice"] > 0]
    df.dropna(subset=["InvoiceDate"], inplace=True)

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%d/%m/%y %H:%M")

    db["clean_data"].drop()
    db["clean_data"].insert_many(df.to_dict(orient="records"))


if __name__ == "__main__":
    clean_data()
