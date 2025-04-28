#include "Controller.h"

Controller::Controller()
{
    instance = this;
}

Controller* Controller::instance = nullptr;

void Controller::setup()
{
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
    if (commands[0].equals(message)){
        instance->audioClient_.updatePosition(-1);
    }
    else if (commands[1].equals(message)){
        instance->audioClient_.updatePosition(1);
    }
    else if  (commands[2].equals(message)){
        instance->audioClient_.pause();
    }
    else{
        float volume = message.toFloat();
        instance->audioClient_.updateVolume(volume);
    }
  
    Serial.println("");
}
