FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY main.py .

RUN pip install --no-cache-dir fastapi "uvicorn[standard]" kafka-python

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
