FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY kafka-producer/producer.py .

COPY utils /app/utils

RUN pip install --no-cache-dir kafka-python

CMD ["python", "producer.py"]
