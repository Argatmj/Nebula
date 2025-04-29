#include "WebServerSocket.h"

WebServerSocket::WebServerSocket():
server_(80),
webSocket_(WebSocketsServer(1337))
{
    instance = this;
}

void WebServerSocket::loop()
{
    webSocket_.loop();
}

void WebServerSocket::setup()
{
    Serial.begin(115200);
  if( !SPIFFS.begin()){
    Serial.println("Error mounting SPIFFS");
    while(1);
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected.");
  
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());

  server_.on("/", HTTP_GET, onIndexRequest);
  server_.on("/style.css", HTTP_GET, onCSSRequest);
  server_.onNotFound(onPageNotFound);

  server_.begin();
  webSocket_.begin();
  webSocket_.onEvent(onEvent);
}

WebServerSocket* WebServerSocket::instance = nullptr;

void WebServerSocket::onEvent(uint8_t client_num, WStype_t type, uint8_t *payload, size_t length)
{
    switch (type) {
        case WStype_DISCONNECTED:
          Serial.printf("[%u] Disconnected!\n", client_num);
          break;
        case WStype_CONNECTED:
        {
          IPAddress ip = instance->webSocket_.remoteIP(client_num);
          Serial.printf("[%u] Connection from ", client_num);
          Serial.println(ip.toString());
          break;
        }
        case WStype_TEXT:
        {
          String message;
          for (unsigned int i = 0; i < length; i++) {
            message += (char)payload[i];
          }
          message.trim();
          Serial.println(message);
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

void WebServerSocket::onIndexRequest(AsyncWebServerRequest *request)
{
    IPAddress remote_ip = request->client()->remoteIP();
    Serial.println("[" + remote_ip.toString() +
                    "] HTTP GET request of " + request->url());
    request->send(SPIFFS, "/index.html", "text/html");
}

void WebServerSocket::onCSSRequest(AsyncWebServerRequest *request)
{
    IPAddress remote_ip = request->client()->remoteIP();
    Serial.println("[" + remote_ip.toString() +
                    "] HTTP GET request of " + request->url());
    request->send(SPIFFS, "/style.css", "text/css");
}

void WebServerSocket::onPageNotFound(AsyncWebServerRequest *request)
{
    IPAddress remote_ip = request->client()->remoteIP();
    Serial.println("[" + remote_ip.toString() +
                    "] HTTP GET request of " + request->url());
    request->send(404, "text/plain", "Not found");
}
