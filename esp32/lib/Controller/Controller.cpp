#include "Controller.h"

Controller::Controller()
{
    instance = this;
}

Controller* Controller::instance = nullptr;

void Controller::setup()
{
    setup_WiFi();
    mqClient_.setup();
    mqClient_.setCallBack(callback);
    audioClient_.setup();
}

void Controller::loop()
{
    mqClient_.loop();
    audioClient_.play();
}

void Controller::callback(char *topic, byte *payload, unsigned int length)
{
    std::vector<String> commands = {"Previous", "Next", "Switch"};
    String message;
    for (unsigned int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    message.trim();

    
    if (strcmp(topic, "Urls") == 0) {
        Serial.println(message);
        instance->audioClient_.addAudio(message.c_str());  
        Serial.println("Added Audio.");
        return;
    }

    if (strcmp(topic, "Volume") == 0) {
        float volume = message.toFloat();
        instance->audioClient_.updateVolume(volume);
        Serial.println("Volume Updated.");
        return;
    }

    if (commands[0].equals(message)){
        instance->audioClient_.updatePosition(-1);
        Serial.println("Previous Audio.");
    }
    else if (commands[1].equals(message)){
        instance->audioClient_.updatePosition(1);
        Serial.println("Next Audio.");
    }
    else if  (commands[2].equals(message)){
        instance->audioClient_.pause();
        Serial.println("Switched");
    }
  
    Serial.println("");
}

void Controller::setup_WiFi()
{
    Serial.println();
    Serial.print("Connecting to WiFi");
    Serial.println(ssid_);
  
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid_, password_);
  
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
   
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
