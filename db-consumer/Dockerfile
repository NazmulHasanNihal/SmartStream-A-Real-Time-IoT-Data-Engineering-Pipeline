FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY write_to_postgres.py .

RUN pip install --no-cache-dir kafka-python psycopg2-binary

CMD ["python", "write_to_postgres.py"]
