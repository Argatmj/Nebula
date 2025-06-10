#include <vector>
#include <string.h>
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
    void setup_WiFi();
    void reconnect();
    WiFiClient espClient_;
    PubSubClient mqClient_;
    const char* mqtt_server_ = MQTT_IP;
    void subscribeToTopics(PubSubClient& client, std::vector<String> topics = {"Position","State","Volume","Urls"});
};