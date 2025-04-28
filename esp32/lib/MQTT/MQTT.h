#include <vector>
#include <string.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>

#define MQTT_CALLBACK_SIGNATURE std::function<void(char*, uint8_t*, unsigned int)> callback

class MQTT {
    public:
    MQTT();
    void setup();
    void loop();
    void setCallBack(MQTT_CALLBACK_SIGNATURE);
    
    private:
    void reconnect();
    void setup_Wifi();
    WiFiClient espClient_;
    PubSubClient mqClient_;
    const char* ssid_ = "";
    const char* password_ = "";
    const char* mqtt_server_ = "";
    void subscribeToTopics(PubSubClient& client, std::vector<String> topics = {"Position","State","Volume"});
};