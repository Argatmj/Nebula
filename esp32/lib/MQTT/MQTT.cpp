#include "MQTT.h"

MQTT::MQTT():
client_(espClient_)
{}

void MQTT::setup()
{
    setup_Wifi();
    client_.setServer(mqtt_server_, 1883);
    client_.setCallback(MQTT::callback);
}

void MQTT::loop()
{
    if (!client_.connected()) {
        reconnect();
        subscribeToTopics(client_);
    }
    client_.loop();
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

void MQTT::callback(char *topic, byte* payload, unsigned int length)
{
    std::vector<String> commands = {"Previous", "Next", "Switch"};
    String message;
    for (unsigned int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    message.trim();
    if (commands[0].equals(message)){
        Serial.println("prev");
    }
    else if (commands[1].equals(message)){
        Serial.println("next");
    }
    else if  (commands[2].equals(message)){
        Serial.println("switch");
    }
    else{
        Serial.println(message);    
    }
  
    Serial.println("");
}

void MQTT::reconnect()
{
    while (!client_.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    if (client_.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client_.state());
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

