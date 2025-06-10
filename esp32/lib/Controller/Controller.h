#include "MQTT.h"
#include <WiFi.h>
#include "AudioPC.h"
#include "WebServerSocket.h"

class Controller {
    public:
    Controller();
    void setup();
    void loop();
    static Controller* instance;
    static void callback(char* topic, byte* payload, unsigned int length);
    static void onEvent(uint8_t client_num,WStype_t type,uint8_t * payload, size_t length);

    private:
    MQTT mqClient_;
    void setup_WiFi();
    AudioPC audioClient_;
    bool isNumber(String str);
    WebServerSocket webClient_;
    const char* ssid_ = WIFI_SSID;
    const char* password_ = WIFI_PASSWORD;
};