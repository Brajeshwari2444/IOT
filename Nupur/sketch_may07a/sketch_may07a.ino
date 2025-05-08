#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "Nadella 2.4G";
const char* password = "Tomjerry";

// MQTT broker info
const char* mqtt_server = "192.168.29.86";
const int mqtt_port = 1883;
const char* mqtt_topic = "iot/fire_gas";


#define MQ2PIN 34
#define FIREPIN 35

// Static location label
const char* location = "indoor";

// WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);


void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void connect_wifi(){
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void setup() {
  Serial.begin(115200);
  connect_wifi();
  pinMode(MQ2PIN, INPUT);
  pinMode(FIREPIN, INPUT);
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();
  
  float mq2Val = analogRead(MQ2PIN);
  float fireVal = analogRead(FIREPIN);

  if (isnan(mq2Val) || isnan(fireVal)) {
    Serial.println("Failed to read from MQ2 sensor!");
    return;
  }

  // Prepare JSON payload
  StaticJsonDocument<256> doc;
  doc["device_id"] = "fire_gas_01";
  doc["location"] = location;
  doc["mq2"] = (mq2Val/4096)*100;
  doc["fire"] = 4095-fireVal;

  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);
  
  Serial.print("Published: ");
  Serial.println(jsonBuffer);
  client.publish(mqtt_topic, jsonBuffer);
  delay(500);
}
