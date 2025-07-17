FROM apache/airflow:2.7.2-python3.10

USER root
RUN apt-get update && apt-get install -y gcc g++ libssl-dev

USER airflow

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt