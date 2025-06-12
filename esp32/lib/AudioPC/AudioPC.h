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
    const char *urls[4] = {
        "https://strm112.1.fm/bossanova_mobile_mp3?aw_0_req.gdpr=true",
        "https://npr-ice.streamguys1.com/live.mp3",
        "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
        "http://ice1.somafm.com/groovesalad-128-mp3"
      };
      
    const char *wifi = WIFI_SSID;
    const char *password = WIFI_PASSWORD;
    
    URLStream urlStream_;
    AudioSourceDynamicURL source_;
    I2SStream i2s_;
    MP3DecoderHelix decoder_;
    AudioPlayer player_;
};