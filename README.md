# E-Commerce Sales Forecasting Pipeline

An end-to-end data pipeline for forecasting 30-day online retail sales using real transactional data. Built with Apache Airflow, Facebook Prophet, MongoDB Atlas, Docker, and Flask — and deployed on Render for live dashboarding.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Pipeline Flow](#pipeline-flow)
- [Model Details](#model-details)
- [Dashboard Features](#dashboard-features)
- [Cloud Deployment](#cloud-deployment)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## Overview

This project solves the problem of short-term demand forecasting for online retailers. It forecasts total daily revenue for the next 30 days, using historical sales data, and delivers interactive visual insights through a deployed dashboard.

---

## Tech Stack

| Layer         | Technology                            |
|--------------|----------------------------------------|
| Orchestration | Apache Airflow (Dockerized)           |
| Data Storage  | MongoDB Atlas (Cloud NoSQL)           |
| Forecasting   | Facebook Prophet                      |
| Dashboard     | Flask + Plotly                        |
| Deployment    | Docker Compose + Render               |
| DevOps        | .env secrets + GitHub CI ready        |

---

## Architecture

```text
[CSV File] 
   ↓
[ETL & Aggregation (Python + Airflow)]
   ↓
[Cleaned Data → MongoDB Atlas]
   ↓
[Forecast using Prophet]
   ↓
[Predictions CSV → Flask App (Render)]
   ↓
[Interactive Dashboard (Plotly)]
```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Docker & Docker Compose
- MongoDB Atlas account
- Render account (for deployment)

### Clone Repository

```bash
git clone 
cd ecommerce-forecasting-pipeline
```

### Setup Environment

Create a `.env` file in root directory:

```env
MONGO_URI=mongodb+srv://Saikiran_ML:tech@cluster0.ay5okke.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

### Start Services Locally

```bash
docker-compose up --build
```

Access Airflow UI at: `http://localhost:8080`  
Access Dashboard at: `http://localhost:5000`

---

## Pipeline Flow

1. CSV data is ingested into MongoDB
2. Daily revenue aggregated per day
3. Prophet forecasts 30 days of future revenue
4. Results saved to `prediction.csv`
5. Dashboard reads this file and renders it with filters & KPIs

---

## Model Details

- Model: Facebook Prophet
- Input: Aggregated daily revenue
- Horizon: 30-day future forecast
- Output: `ds`, `yhat`, `yhat_lower`, `yhat_upper`

---

## Dashboard Features

- Line chart of predicted sales
- Dropdown filters for Country & Product (if present)
- KPI cards for total sales
- Hover tooltips with confidence intervals
- Download forecast data as CSV

---

## Cloud Deployment

### MongoDB Atlas

- Cloud-hosted NoSQL database
- Stores both raw transactions and aggregated data
- Connection handled via MONGO_URI in `.env`

### Render (Flask Dashboard)

- Deployed from GitHub via render.yaml
- Auto-deploys on commit
- Environment variables securely configured in dashboard

```yaml
services:
  - type: web
    name: ecommerce-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: MONGO_URI
        value: mongodb+srv://Saikiran_ML:tech@cluster0.ay5okke.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

```

---

## Future Improvements

- Add holiday regressors to Prophet
- Move from batch to real-time with Kafka & Spark Streaming
- Auto-retrain model daily using CI/CD
- Add role-based login for dashboard

---

## Authors

- Harsha Vijaya Kumar – Airflow DAGs, project documentation, deployment
- Saikiran Magadi Lakshmeesha – ETL pipelines, Flask dashboard
- Durgaprasad Sunkara – Docker orchestration, MongoDB integration
- Supreetha Devagiri – ML modeling with Prophet, hyperparameter tuning

---

## License

[MIT License](https://mit-license.org/)

---

## Contact

Have questions or suggestions? Feel free to contact us via GitHub or email.
