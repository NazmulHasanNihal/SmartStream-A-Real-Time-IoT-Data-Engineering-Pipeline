import json
import time
from datetime import datetime
import psycopg2
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaError

# Assign region based on device ID
def assign_region(device_id):
    num = int(device_id.split("-")[1])
    return "north" if num <= 5 else "south"

# Retry Kafka connection
for _ in range(10):
    try:
        consumer = KafkaConsumer(
            'iot-sensor-processed',
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='db-writer'
        )
        print("✅ Connected to Kafka")
        break
    except NoBrokersAvailable:
        print("❌ Kafka not ready, retrying in 5s...")
        time.sleep(5)
else:
    raise RuntimeError("❌ Kafka is not available after 10 attempts.")

# Retry Postgres connection
for _ in range(10):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='nC3myTyj1UKaDJbV',
            host='aws-0-ap-south-1.pooler.supabase.com',
            port='6543'
        )
        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL")
        break
    except psycopg2.OperationalError:
        print("❌ Postgres not ready, retrying in 5s...")
        time.sleep(5)
else:
    raise RuntimeError("❌ PostgreSQL is not available after 10 attempts.")

print("🚀 Database Consumer is running...")

try:
    for message in consumer:
        data = message.value
        try:
            # Add region if missing
            if "region" not in data:
                data["region"] = assign_region(data["device_id"])

            cursor.execute(
                """
                INSERT INTO sensor_readings
                (device_id, temperature, humidity, battery, status, region, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data["device_id"],
                    float(data["temperature"]),
                    float(data["humidity"]),
                    float(data["battery"]),
                    data["status"],
                    data["region"],
                    datetime.fromisoformat(data["timestamp"])
                )
            )
            conn.commit()
            print(f"✅ Inserted: {data}")
        except Exception as e:
            print(f"❌ Insert Error: {e}")
            conn.rollback()

except KeyboardInterrupt:
    print("🛑 Stopped by user.")

finally:
    cursor.close()
    conn.close()
    print("🔒 DB connection closed.")
