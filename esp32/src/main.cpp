#include "AudioPC.h"

AudioPC audio;

void setup() {
  Serial.begin(115200);
  audio.setup();
}
void loop() {
  audio.play();
}