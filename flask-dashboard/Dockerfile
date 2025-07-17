FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install flask pandas plotly pymongo pymongo[srv] python-dotenv

CMD ["python", "app.py"]
