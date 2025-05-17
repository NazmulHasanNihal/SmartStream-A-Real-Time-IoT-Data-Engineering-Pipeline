from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
import json

def assign_region(device_id):
    """Dummy region assignment based on device_id"""
    num = int(device_id.split("-")[1])
    return "north" if num <= 5 else "south"

def process(stream):
    return (stream
        .map(lambda x: json.loads(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))
        .filter(lambda d: d['status'] != 'error')
        .map(lambda d: {**d, 'region': assign_region(d['device_id'])},
             output_type=Types.MAP(Types.STRING(), Types.STRING()))
        .map(lambda d: json.dumps(d), output_type=Types.STRING())
    )

env = StreamExecutionEnvironment.get_execution_environment()

kafka_props = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'flink-processor'
}

source = FlinkKafkaConsumer(
    topics='iot-sensor-raw',
    deserialization_schema=SimpleStringSchema(),
    properties=kafka_props
)

sink = FlinkKafkaProducer(
    topic='iot-sensor-processed',
    serialization_schema=SimpleStringSchema(),
    producer_config={'bootstrap.servers': 'kafka:9092'}
)

input_stream = env.add_source(source)
output_stream = process(input_stream)
output_stream.add_sink(sink)

env.execute("Flink IoT Stream Processor")
