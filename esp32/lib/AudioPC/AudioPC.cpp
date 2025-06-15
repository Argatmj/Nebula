#include "AudioPC.h"

AudioPC::AudioPC(): 
urlStream_(wifi, password),
source_(urlStream_, urls, "audio/mp3"), // specify source with urls and audio format 
player_(source_, i2s_, decoder_) // create audio player with source, i2s and decoder
{}

// update the playback based on position 
void AudioPC::updatePosition(int pos){
    pos == 1 ? player_.next() : player_.previous();
}

// add new url to the source 
void AudioPC::addAudio(const char* url)
{
    source_.addURL(url);
}

// set the volume to newVolume 
void AudioPC::updateVolume(float newVolume){
    player_.setVolume(newVolume);
}

// toggles play/pause based on current state 
void AudioPC::pause(){
    player_.setActive(!player_.isActive());
    String active = player_.isActive() ? "Active" : "Inactive";
    Serial.print("Current Player Status: ");
    Serial.println(active);
}

// sets I2S configuration 
void AudioPC::setup(){
    auto cfg = i2s_.defaultConfig(TX_MODE);
    cfg.pin_ws = 14; // WS pin
    cfg.pin_bck = 27; // BCK pin
    cfg.pin_data = 26; // DOUT pin
    cfg.buffer_size = 1024;

    i2s_.begin(cfg);
    
    player_.begin();
    player_.setVolume(0.3);
}

// starts audio stream
void AudioPC::play(){
    player_.copy();
}