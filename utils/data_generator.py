import random
from datetime import datetime

def generate_sensor_data():
    device_id = f"sensor-{random.randint(1, 10):02d}"
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(15, 40), 2),
        "humidity": round(random.uniform(20, 90), 2),
        "battery": round(random.uniform(10, 100), 1),
        "status": random.choice(["active", "idle", "error"]),
        "timestamp": datetime.utcnow().isoformat(),
    }
