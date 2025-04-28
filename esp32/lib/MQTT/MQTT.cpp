#include "MQTT.h"

MQTT::MQTT():
mqClient_(espClient_)
{
}

void MQTT::setup()
{
    setup_Wifi();
    mqClient_.setServer(mqtt_server_, 1883); 
}

void MQTT::loop()
{
    if (!mqClient_.connected()) {
        reconnect();
        subscribeToTopics(mqClient_);
    }
    mqClient_.loop();
}

void MQTT::setCallBack(MQTT_CALLBACK_SIGNATURE)
{
  mqClient_.setCallback(callback);
}

void MQTT::setup_Wifi()
{
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid_);
  
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid_, password_);
  
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
  
    randomSeed(micros());
  
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void MQTT::reconnect()
{
    while (!mqClient_.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    if (mqClient_.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqClient_.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void MQTT::subscribeToTopics(PubSubClient &client, std::vector<String> topics)
{
    for (auto& topic : topics){
        client.subscribe(topic.c_str());
      }
}

