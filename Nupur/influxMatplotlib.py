import matplotlib.pyplot as plt
import json
from datetime import datetime
import paho.mqtt.client as mqtt
from influxdb_client_3 import InfluxDBClient3, Point
import pandas as pd

# InfluxDB 3.x Connection Info
INFLUX_URL = "http://localhost:8181"
INFLUX_TOKEN = ""  # Leave blank if auth-mode is disabled
INFLUX_DATABASE = "influxDbNew"

# MQTT Broker Info
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/temperature"

# Connect to InfluxDB 3.x
influx_client = InfluxDBClient3(
    host=INFLUX_URL,
    token=INFLUX_TOKEN,
    database=INFLUX_DATABASE
)








## Query recent temperature data from InfluxDB 3.x
# query = """
# SELECT temperature, time
# FROM temperature_data
# WHERE time > now() - interval '1 hour'
# ORDER BY time ASC
# """



query = "SELECT * FROM fire_gas"
result = influx_client.query(query)

print(len(result))

# Convert to Pandas DataFrame
df = result.to_pandas()
df.to_csv("InfluxToCSV.csv")
print(df.columns)


if not {"time", "mq2", "fire"}.issubset(df.columns):
    print("Missing expected columns in data.")
else:
    # Convert time column to datetime if not already
    df["time"] = pd.to_datetime(df["time"])

    # Plot by location
    plt.figure(figsize=(10, 5))

    for location, group in df.groupby("location"):
        plt.plot(
            group["time"],
            group["mq2"],
            marker='o',
            linestyle='-',
            label=location
        )

    plt.xlabel("Timestamp")
    plt.ylabel("MQ2 gas sensor data")
    plt.title("Gas sensor data")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()