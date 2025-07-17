# app.py
from flask import Flask, render_template, send_file
import pandas as pd
import plotly.graph_objs as go
import plotly
import json
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# CSV_PATH = "airflow/scripts/static/predictions.csv"


@app.route("/")
def index():

    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ecommerce"]

    # Read with BOM handling and clean columns
    df = pd.DataFrame(list(db["forecast"].find()))
    df.columns = df.columns.str.strip()  # Remove whitespace in column names

    # Ensure 'ds' is datetime and normalized to remove time component
    df["ds"] = pd.to_datetime(df["ds"]).dt.normalize()
    df.sort_values("ds", inplace=True)

    # Drop invalid or missing forecast values
    df.dropna(subset=["ds", "yhat", "yhat_lower", "yhat_upper"], inplace=True)

    # Round and convert forecast values to int
    df["yhat"] = df["yhat"].round().astype(int)
    df["yhat_lower"] = df["yhat_lower"].round().astype(int)
    df["yhat_upper"] = df["yhat_upper"].round().astype(int)

    # KPIs
    total_forecast = round(df["yhat"].sum(), 2)
    avg_daily = round(df["yhat"].mean(), 2)
    forecast_days = df["ds"].nunique()

    # Aggregate total forecast sales by month
    monthly_sales = df.groupby(pd.Grouper(key="ds", freq="M"))["yhat"].sum().reset_index()

    # Create Plotly figure
    fig = go.Figure()

    # Monthly forecast line
    fig.add_trace(
        go.Scatter(
            x=monthly_sales["ds"],  # Keep datetime for slider support
            y=list(monthly_sales["yhat"]),
            mode="lines+markers+text",
            name="Monthly Total Forecast",
            line=dict(color="#FF7F0E", width=3),
            hovertemplate="Month: %{x|%b %Y}<br>Sales: £%{y:,.0f}<extra></extra>",
        )
    )

    # Layout
    fig.update_layout(
        title=dict(
            text="<b>📈 Monthly Sales Forecast</b>",
            font=dict(size=24),
            x=0.03,
            y=0.95,
        ),
        xaxis=dict(
            title="Month",
            rangeselector=dict(
                buttons=[
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            ),
            rangeslider=dict(visible=True),
            type="date",
            tickformat="%b %Y",
            tickangle=0,
        ),
        yaxis=dict(title="Sales (£)", tickprefix="£", gridcolor="lightgrey"),
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=100, b=40),
        plot_bgcolor="rgba(248,248,248,0.9)",
    )

    # Convert figure to JSON for rendering in dashboard.html
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Get today's date
    forecast_date = datetime.now().strftime("%d %b %Y")

    return render_template(
        "dashboard.html",
        graphJSON=graphJSON,
        total_forecast=f"{total_forecast:,.2f}",
        avg_daily=f"{avg_daily:,.2f}",
        forecast_days=forecast_days,
        forecast_date=forecast_date,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4500)
