import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def process_data():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ecommerce"]

    # Load cleaned data from MongoDB
    df = pd.DataFrame(list(db["clean_data"].find()))

    # Calculate total sales per record
    df["Total"] = df["Quantity"] * df["UnitPrice"]

    # Convert InvoiceDate to datetime (keep your original line)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%d/%m/%y %H:%M")

    # Filter out cancelled orders (InvoiceNo starting with 'C')
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Aggregate total sales by date (date only, no time)
    daily = df.groupby(df["InvoiceDate"].dt.date)["Total"].sum().reset_index()

    # Rename columns for Prophet
    daily.columns = ["ds", "y"]

    # Fill missing dates in the time series with zero sales
    all_dates = pd.date_range(start=daily["ds"].min(), end=daily["ds"].max())
    daily = (
        daily.set_index("ds")
        .reindex(all_dates, fill_value=0)
        .rename_axis("ds")
        .reset_index()
    )

    # Save the processed daily sales time series back to MongoDB
    db["timeseries"].drop()
    db["timeseries"].insert_many(daily.to_dict(orient="records"))

    print(f"Processed {len(daily)} daily records saved to 'timeseries' collection.")


if __name__ == "__main__":
    process_data()
