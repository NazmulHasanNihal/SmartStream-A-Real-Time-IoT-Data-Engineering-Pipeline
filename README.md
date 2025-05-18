# 📡 SmartStream: A Real Time IoT Data Engineering Pipeline
A real-time IoT data pipeline using Kafka, Flink, PostgreSQL, FastAPI, and Streamlit. Simulates sensor data, processes streams with Flink, stores results in PostgreSQL, serves live data via WebSocket API, and visualizes metrics on a real-time dashboard. Fully Dockerized.

![Smart Stream Dashboard](SmartStreamDashboard.gif)


## 🎯 Project Motive
In today’s digital world, millions of IoT devices produce sensor data every second. Companies need real-time pipelines to monitor, process, and act on this data instantly. This project was built to demonstrate the practical skills needed to engineer a real-time data pipeline from ingestion to dashboard using modern tools.

## ❓ Problem / Research Question
**How can we build a scalable and reliable real-time data pipeline to simulate, process, store, and visualize IoT sensor data using open-source tools?**

## 🧱 Architecture
```markdown
                                   [Simulated Sensors]
                                            ↓
                                 [Kafka (iot-sensor-raw)]
                                            ↓
                                 [Flink: Filter + Enrich]
                                            ↓
                              [Kafka (iot-sensor-processed)]
                                            ↓
                                  [PostgreSQL Storage]
                                            ↓            
                                   [FastAPI WebSocket] 
                                            ↓
                                  [Streamlit Dashboard]
```

## 🛠️ Tools & Technologies Used
| Tool               | Purpose                                      |
| ------------------ | -------------------------------------------- |
| **Python**         | `Simulate IoT data, Kafka producer & consumer` |
| **Apache Kafka**   | `Real-time data streaming`                     |
| **Apache Flink**   | `Stream processing and data enrichment`        |
| **PostgreSQL**     | `Persistent storage of processed data `        |
| **FastAPI**        | `Real-time WebSocket API`                      |
| **Streamlit**      | `Real-time dashboard`                          |
| **Docker**         | `Containerization of the full stack`           |
| **Docker Compose** | `Service orchestration`                        |


## 📁 Project Structure: `SmartStream: A Real Time IoT Data Engineering Pipeline/`
```markdown
SmartStream: A Real Time IoT Data Engineering Pipeline/
├── docker-compose.yml              # Orchestrates all services
├── requirements.txt                # Combined Python dependencies

├── utils/
│   └── data_generator.py           # Simulates realistic IoT sensor data

├── kafka-producer/
│   ├── producer.py                 # Streams simulated data to Kafka
│   └── Dockerfile                  # Dockerized Python Kafka producer

├── flink-job/
│   └── flink_processing_job.py     # PyFlink job: filters + enriches data

├── db-consumer/
│   ├── write_to_postgres.py        # Kafka consumer to save data to PostgreSQL
│   └── Dockerfile                  # Dockerfile for the DB writer

├── api-server/
│   ├── main.py                     # FastAPI WebSocket for live data streaming
│   └── Dockerfile                  # WebSocket API container

├── dashboard/
│   ├── app.py                      # Streamlit real-time dashboard
│   └── Dockerfile                  # Streamlit service container

├── init.sql                        # SQL schema for PostgreSQL table
├── README.md                       # Full project overview, instructions, usage
└── .gitignore                      # (Optional) Ignore venvs, pycache, logs, etc.

```

## 📦 What I Built (Step-by-Step)

- **✅ 1. Simulated IoT Sensor Data**

  - `Wrote a Python script to simulate sensor data (device_id, temperature, humidity, battery, status, region, timestamp).`

  - `Streamed it to a Kafka topic iot-sensor-raw.`

- **✅ 2. Kafka Message Broker**

  - `Used Kafka + Zookeeper to ingest and queue real-time messages.`

- **✅ 3. Stream Processing with Flink**

  - `Builted a PyFlink job to filter out error data and enrich each record with a region label.`

  - `Wroted clean data to a new Kafka topic: iot-sensor-processed.`

- **✅ 4. PostgreSQL Database**

  - `Created a sensor_readings table using SQL schema.`

  - `Builted a Python Kafka consumer that inserts streamed messages into the database.`

- **✅ 5. FastAPI WebSocket API**

  - `Created a WebSocket endpoint at /ws/sensor-stream.`

  - `Streaming data from Kafka directly to connected clients in real time.`

- **✅ 6. Streamlit Dashboard**

  - `Live charts for temperature, humidity, and device statuses.`

  - `Auto-refreshes every few seconds by reading from PostgreSQL.`

- **✅ 7. Docker Compose Orchestration**

  - `Builted the entire system as a multi-service Docker project.`

  - `One command spins up Kafka, Flink, PostgreSQL, producer, API, and dashboard.`

## ✅ Project Outcomes

- **✅ Real-time data simulation and ingestion**

- **✅ Data filtering, enrichment, and processing**

- **✅ Persistent storage for historical data analysis**

- **✅ Live data access via API**

- **✅ Visual insights via dashboard**

- **✅ All services containerized and reproducible**

## 📈 Real-World Applications

- `Smart home monitoring`

- `Manufacturing & industrial sensors`

- `Health and fitness trackers`

- `Logistics and GPS systems`

- `Environmental data analytics`

## 🧳 What This Demonstrates

**This project showcases my skills in:**

- `Real-time data engineering`

- `Streaming architecture`

- `Kafka topic design and consumption`

- `Stream processing logic (Flink)`

- `Data warehousing with PostgreSQL`

- `API engineering (FastAPI WebSocket)`

- `Dashboard design (Streamlit)`

- `Docker orchestration & DevOps basics`

## 🧩 Future Enhancements

- `Integrate with Grafana + Prometheus`

- `Cloud deployment (AWS / GCP / Azure)`

- `Add alerting logic for threshold breaches`

- `Add historical trends page in dashboard`

- `Add authentication for the API`

## 🧰 How to Run the Project
```markdown
git clone <https://github.com/NazmulHasanNihal/SmartStream-A-Real-Time-IoT-Data-Engineering-Pipeline.git>
cd iot-kafka-pipeline
docker-compose up --build
```
- **WebSocket API:** `ws://localhost:8000/ws/sensor-stream`

- **Dashboard:** `http://localhost:8501`

- **PostgreSQL:** `localhost:5432 with user iot_user, password iot_pass`

## Requirements `requirements.txt`
```markdown
kafka-python
psycopg2-binary
sqlalchemy
fastapi
uvicorn
streamlit
pandas
apache-flink
altair
```
### 🔧 How to Use
**Bash**
```bash
pip install -r requirements.txt
```
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

## 📃 License

MIT License