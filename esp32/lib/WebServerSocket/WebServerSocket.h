#include <WiFi.h>
#include <SPIFFS.h>
#include <ESPAsyncWebServer.h>
#include <WebSocketsServer.h>

class WebServerSocket{
    public:
    WebServerSocket();
    void loop();
    void setup();
    static WebServerSocket* instance;
    static void onEvent(uint8_t client_num,WStype_t type,uint8_t * payload, size_t length);

    private:
    AsyncWebServer server_;
    WebSocketsServer webSocket_;
    const char *ssid = "";
    const char *password =  "";
    static void onIndexRequest(AsyncWebServerRequest *request);
    static void onCSSRequest(AsyncWebServerRequest *request);
    static void onPageNotFound(AsyncWebServerRequest *request);

};