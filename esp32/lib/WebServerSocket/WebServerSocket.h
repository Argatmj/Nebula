#include <SPIFFS.h>
#include <ESPAsyncWebServer.h>
#include <WebSocketsServer.h>

#define WebServerSocket_On_Event std::function<void(uint8_t num, WStype_t type, uint8_t * payload, size_t length)> onEvent

class WebServerSocket{
    public:
    WebServerSocket();
    void loop();
    void setup();
    IPAddress getIP(uint8_t client_num);
    void setOnEvent(WebServerSocket_On_Event);

    private:
    AsyncWebServer server_;
    WebSocketsServer webSocket_;
    static void onIndexRequest(AsyncWebServerRequest *request);
    static void onCSSRequest(AsyncWebServerRequest *request);
    static void onPageNotFound(AsyncWebServerRequest *request);
};