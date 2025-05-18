import random
from datetime import datetime

def generate_sensor_data():
    return {
        "device_id": f"sensor-{random.randint(1, 10):02d}",
        "temperature": round(random.uniform(15, 40), 2),
        "humidity": round(random.uniform(20, 90), 2),
        "battery": round(random.uniform(10, 100), 1),
        "status": random.choice(["active", "idle", "error"]),
        "region": random.choice(["north", "south", "east", "west"]),  # ✅ ADD THIS
        "timestamp": datetime.utcnow().isoformat()
    }
