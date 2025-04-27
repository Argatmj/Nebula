#include <vector>
#include <string.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>

class MQTT {
    public:
    MQTT();
    void setup();
    void loop();
    

    private:
    void reconnect();
    void setup_Wifi();
    WiFiClient espClient_;
    PubSubClient client_;
    const char* ssid_ = "";
    const char* password_ = "";
    const char* mqtt_server_ = "";
    static void callback(char* topic, byte* payload, unsigned int length);
    void subscribeToTopics(PubSubClient& client, std::vector<String> topics = {"Position","State","Volume"});
};