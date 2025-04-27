#include "AudioTools.h"
#include "AudioTools/AudioCodecs/CodecMP3Helix.h"
#include "AudioTools/Disk/AudioSourceURL.h"


class AudioPC {
    public:
    AudioPC();
    void updateVolume(float newVolume);
    void updatePosition(int pos);
    void pause();
    void play();
    void setup();

    private:
    const char *urls[5] = {
        "http://stream.srg-ssr.ch/m/rsj/mp3_128",
        "http://stream.srg-ssr.ch/m/drs3/mp3_128",
        "http://stream.srg-ssr.ch/m/rr/mp3_128",
        "http://streaming.swisstxt.ch/m/drsvirus/mp3_128",
        "https://strm112.1.fm/bossanova_mobile_mp3?aw_0_req.gdpr=true"
      };
      
    const char *wifi = "";
    const char *password = "";

    URLStream urlStream_;
    AudioSourceURL source_;
    I2SStream i2s_;
    MP3DecoderHelix decoder_;
    AudioPlayer player_;
};