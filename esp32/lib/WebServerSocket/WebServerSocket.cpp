#include "WebServerSocket.h"


WebServerSocket::WebServerSocket():
server_(80),
webSocket_(WebSocketsServer(1337))
{
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
  server_.on("/", MY_HTTP_GET, onIndexRequest);
  server_.on("/style.css", MY_HTTP_GET, onCSSRequest);
  server_.onNotFound(onPageNotFound);

  server_.begin();
  webSocket_.begin();
}

void WebServerSocket::setOnEvent(WebServerSocket_On_Event)
{
  webSocket_.onEvent(onEvent);
}

IPAddress WebServerSocket::getIP(uint8_t client_num)
{
    return webSocket_.remoteIP(client_num);
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
