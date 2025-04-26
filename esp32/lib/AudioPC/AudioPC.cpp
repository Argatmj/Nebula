#include "AudioPC.h"

AudioPC::AudioPC(): 
urlStream_(wifi, password),
source_(urlStream_, urls, "audio/mp3"),
player_(source_, i2s_, decoder_)
{}

void AudioPC::updatePosition(int pos){
    pos == 1 ? player_.next() : player_.previous();
}

void AudioPC::updateVolume(float newVolume){
    player_.setVolume(newVolume);
}

void AudioPC::pause(){
    player_.setActive(player_.isActive());
}

void AudioPC::setup(){
    auto cfg = i2s_.defaultConfig(TX_MODE);
    cfg.pin_ws = 14;
    cfg.pin_bck = 27;
    cfg.pin_data = 26;

    i2s_.begin(cfg);

    player_.begin();
    player_.setVolume(0.3);
}

void AudioPC::play(){
    player_.copy();
}