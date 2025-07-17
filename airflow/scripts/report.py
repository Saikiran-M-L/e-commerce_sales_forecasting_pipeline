import os
import pickle
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def generate_report():
    # MongoDB setup
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ecommerce"]

    # Load training data to get last date
    df = pd.DataFrame(list(db["timeseries"].find()))
    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
    df = df.dropna(subset=["ds"])

    if df.empty:
        raise ValueError("❌ No data available in 'timeseries' collection.")

    # Load trained Prophet model
    model_path = "/opt/airflow/scripts/model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model file not found at {model_path}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Generate 30-day forecast
    future = model.make_future_dataframe(periods=30, freq="D")
    forecast = model.predict(future)

    # Select relevant forecast columns
    output = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

    # Save to CSV for Flask dashboard
    csv_path = "/opt/airflow/scripts/static/predictions.csv"
    output.to_csv(csv_path, index=False)

    # (Optional) Save to MongoDB for web querying
    db["forecast"].drop()
    db["forecast"].insert_many(output.to_dict(orient="records"))

    print(f"✅ Forecast saved to {csv_path}")
    print("✅ Forecast inserted into MongoDB collection: 'forecast'")


if __name__ == "__main__":
    generate_report()
