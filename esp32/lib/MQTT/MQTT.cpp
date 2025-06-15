#include "MQTT.h"

MQTT::MQTT():
mqClient_(espClient_)
{
}

// connect to the mqtt server at port 1883
void MQTT::setup()
{
    mqClient_.setServer(mqtt_server_, 1883);
}

// maintains MQTT connection 
void MQTT::loop()
{
    if (!mqClient_.connected()) {
        reconnect();
        subscribeToTopics(mqClient_);
    }
    mqClient_.loop();
}

// sets the callback function 
void MQTT::setCallBack(MQTT_CALLBACK_SIGNATURE)
{
  mqClient_.setCallback(callback);
}

// reconnect when disconnected 
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

// subscribe to selected topics 
void MQTT::subscribeToTopics(PubSubClient &client, std::vector<String> topics)
{
    for (auto& topic : topics){
        client.subscribe(topic.c_str());
      }
}

