from fastapi import FastAPI, WebSocket
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import os
import asyncio
import threading

app = FastAPI()

KAFKA_TOPIC = "iot-sensor-processed"
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

def consume_kafka_messages(websocket: WebSocket):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            group_id="websocket-client"
        )
        for msg in consumer:
            asyncio.run(websocket.send_json(msg.value))
    except Exception as e:
        print("❌ WebSocket Kafka error:", e)
        asyncio.run(websocket.close())

@app.websocket("/ws/sensor-stream")
async def stream_data(websocket: WebSocket):
    await websocket.accept()
    thread = threading.Thread(target=consume_kafka_messages, args=(websocket,))
    thread.start()
    while thread.is_alive():
        await asyncio.sleep(1)
