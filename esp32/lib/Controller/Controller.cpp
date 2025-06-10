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
    webClient_.setup();
    webClient_.setOnEvent(onEvent);
    audioClient_.setup();
}

void Controller::loop()
{
    mqClient_.loop();
    audioClient_.play();
    webClient_.loop();
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
        Serial.print("Volume: ");
        Serial.println(volume);
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

void Controller::onEvent(uint8_t client_num, WStype_t type, uint8_t *payload, size_t length)
{
    switch (type) {
        case WStype_DISCONNECTED:
            Serial.printf("[%u] Disconnected!\n", client_num);
            break;
        case WStype_CONNECTED:
        {
            IPAddress ip = instance->webClient_.getIP(client_num);
            Serial.printf("[%u] Connection from ", client_num);
            Serial.println(ip.toString());
            break;
        }
        case WStype_TEXT:
        {
            std::vector<String> commands = {"Previous", "Next", "Switch", "http"};
            String message;
            for (unsigned int i = 0; i < length; i++) {
                message += (char)payload[i];
            }
            message.trim();
            
            if (commands[3].equals(message.substring(0, 4))){
                instance->audioClient_.addAudio(message.c_str());  
                Serial.println("Added Audio.");
            }

            if (instance->isNumber(message)){
                float volume = message.toFloat();
                instance->audioClient_.updateVolume(volume);
                Serial.print("Volume: ");
                Serial.println(volume);
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
            break; 
        }
        case WStype_BIN:
        case WStype_ERROR:
        case WStype_FRAGMENT_TEXT_START:
        case WStype_FRAGMENT_BIN_START:
        case WStype_FRAGMENT:
        case WStype_FRAGMENT_FIN:
        default:
          break;
      }
}

void Controller::setup_WiFi(){
    Serial.begin(115200);
    Serial.println();
    Serial.println("ENv:");
    Serial.println(WIFI_SSID);
    Serial.println(WIFI_PASSWORD);    
    Serial.print("Connecting to ");
    Serial.print(ssid_);

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

bool Controller::isNumber(String str) {
    return isDigit(str.charAt(0));
}

  

