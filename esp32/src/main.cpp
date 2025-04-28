#include "Controller.h"

Controller control;

void setup() {
  Serial.begin(115200);
  control.setup();
}

void loop() {
  control.loop();
}