#pragma once
#include "AudioTools.h"
#include "AudioTools/AudioCodecs/CodecMP3Helix.h"
#include "AudioTools/Disk/AudioSourceURL.h"


class AudioPC {
    public:
    AudioPC();
    void updateVolume(float newVolume);
    void updatePosition(int pos);
    void addAudio(const char* url);
    void pause();
    void play();
    void setup();

    private:
    const char *urls[5] = {
        "http://192.168.50.213:8000/blue.mp3",
        "http://192.168.50.213:8000/Bone.mp3",
        "http://192.168.50.213:8000/Fana.mp3",
        "http://192.168.50.213:8000/moon3.mp3",
        "http://192.168.50.213:8000/rush.mp3"
      };
      
    const char *wifi = WIFI_SSID;
    const char *password = WIFI_PASSWORD;
    
    URLStream urlStream_;
    AudioSourceDynamicURL source_;
    I2SStream i2s_;
    MP3DecoderHelix decoder_;
    AudioPlayer player_;
};