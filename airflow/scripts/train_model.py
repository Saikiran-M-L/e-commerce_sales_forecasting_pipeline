import os
import pandas as pd
from pymongo import MongoClient
from prophet import Prophet
import pickle
from dotenv import load_dotenv

load_dotenv()


def train_model():
    # MongoDB setup
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ecommerce"]

    # Load processed daily time series
    df = pd.DataFrame(list(db["timeseries"].find()))
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df = df.dropna(subset=["ds", "y"])

    if df.empty:
        raise ValueError("No valid data found in 'timeseries' collection.")

    # Train Prophet model
    model = Prophet()
    model.fit(df)

    # Save trained model
    model_path = "/opt/airflow/scripts/model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    # Generate future dataframe (90 days)
    future = model.make_future_dataframe(periods=90, freq="D")
    forecast = model.predict(future)

    last_training_date = df["ds"].max()
    output = forecast[forecast["ds"] > last_training_date][
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ]

    # Save to CSV for Flask dashboard
    csv_path = "/opt/airflow/scripts/forecast_90.csv"
    output.to_csv(csv_path, index=False)

    print(f"✅ Model trained and saved to {model_path}")
    print(f"✅ Forecast saved to forecast_90.csv with {len(forecast)} rows")


if __name__ == "__main__":
    train_model()
