#include "AudioPC.h"
#include "MQTT.h"

class Controller {
    public:
    Controller();
    void setup();
    void loop();
    static Controller* instance;
    static void callback(char* topic, byte* payload, unsigned int length);

    private:
    MQTT mqClient_;
    AudioPC audioClient_;
};