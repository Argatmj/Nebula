#include "MQTT.h"

MQTT mq;

void setup() {
  Serial.begin(115200);
  mq.setup();
}

void loop() {
  mq.loop();
}