#include "WebServerSocket.h"

// initializes HTTP server on port 80 and WebSocket on 1337
WebServerSocket::WebServerSocket():
server_(80),
webSocket_(WebSocketsServer(1337))
{
}

// main loop for WebSocket 
void WebServerSocket::loop()
{
    webSocket_.loop();
}

// initialize server and Websocket 
void WebServerSocket::setup()
{
  Serial.begin(115200);
  if( !SPIFFS.begin()){
    Serial.println("Error mounting SPIFFS");
    while(1);
  }
  server_.on("/", MY_HTTP_GET, onIndexRequest); // set route for index file
  server_.on("/style.css", MY_HTTP_GET, onCSSRequest); // set route for style file 
  server_.onNotFound(onPageNotFound); // set route for other files 

  server_.begin();
  webSocket_.begin();
}

// set event handler to the Websocket server
void WebServerSocket::setOnEvent(WebServerSocket_On_Event)
{
  webSocket_.onEvent(onEvent);
}

// get IP address of connected client 
IPAddress WebServerSocket::getIP(uint8_t client_num)
{
    return webSocket_.remoteIP(client_num);
}

// handle request for index file
void WebServerSocket::onIndexRequest(AsyncWebServerRequest *request)
{
    IPAddress remote_ip = request->client()->remoteIP();
    Serial.println("[" + remote_ip.toString() +
                    "] HTTP GET request of " + request->url());
    request->send(SPIFFS, "/index.html", "text/html"); // serve the index.html from SPIFFS
}

// handle request for css file 
void WebServerSocket::onCSSRequest(AsyncWebServerRequest *request)
{
    IPAddress remote_ip = request->client()->remoteIP();
    Serial.println("[" + remote_ip.toString() +
                    "] HTTP GET request of " + request->url());
    request->send(SPIFFS, "/style.css", "text/css"); // serve the style.css from SPIFFS 
}

// handle request for unknown urls 
void WebServerSocket::onPageNotFound(AsyncWebServerRequest *request)
{
    IPAddress remote_ip = request->client()->remoteIP();
    Serial.println("[" + remote_ip.toString() +
                    "] HTTP GET request of " + request->url());
    request->send(404, "text/plain", "Not found"); // serve 404 error 
}
