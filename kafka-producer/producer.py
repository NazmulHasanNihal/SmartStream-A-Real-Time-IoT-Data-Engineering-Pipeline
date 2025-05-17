from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
import sys
import os

sys.path.append('/app/utils')
from data_generator import generate_sensor_data

# Optional: read host from env or default to 'kafka'
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

# Retry logic if Kafka isn't ready
for attempt in range(10):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("✅ Kafka producer connected.")
        break
    except NoBrokersAvailable:
        print("❌ Kafka not available, retrying in 5s...")
        time.sleep(5)
else:
    raise RuntimeError("Kafka is not available after multiple retries.")

# Produce sensor data continuously
try:
    while True:
        data = generate_sensor_data()
        print(f"📤 Produced: {data}")
        producer.send('iot-sensor-processed', value=data)
        time.sleep(1)
except KeyboardInterrupt:
    print("👋 Producer stopped by user.")
finally:
    producer.flush()
    producer.close()
