import json
from datetime import datetime
import paho.mqtt.client as mqtt
from influxdb_client_3 import InfluxDBClient3, Point

# InfluxDB 3.x Connection Info
INFLUX_URL = "http://localhost:8181"
INFLUX_TOKEN = ""  # Leave blank if auth-mode is disabled
INFLUX_DATABASE = "influxDbNew"

# MQTT Broker Info
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/fire_gas"

# Connect to InfluxDB 3.x
influx_client = InfluxDBClient3(
    host=INFLUX_URL,
    token=INFLUX_TOKEN,
    database=INFLUX_DATABASE
)

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("Received:", payload)

        # Parse and write to InfluxDB
        point = (
            Point("fire_gas")
            .tag("device_id", payload["device_id"])
            .tag("location", payload["location"])
            .field("mq2", float(payload["mq2"]))
            .field("fire", float(payload["fire"]))
            .time(datetime.now())
        )

        influx_client.write(point)
        print("Written to InfluxDB")

    except Exception as e:
        print("Error:", e)

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
