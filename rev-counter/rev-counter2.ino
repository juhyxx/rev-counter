#define INPUT_PORT_0 A0
#define INPUT_PORT_1 A1
#define INPUT_PORT_2 A2
#define SENSOR_COUNT 3

struct Rev {
  byte port;
  byte value;
  byte prevValue;
  unsigned long prevTime;
  unsigned long nowTime;
  unsigned long diff;
  float revs;
};
Rev revs[SENSOR_COUNT];
byte i;

void setup() {
  revs[0].port = INPUT_PORT_0;
  revs[1].port = INPUT_PORT_1;
  revs[2].port = INPUT_PORT_2;
  for (i = 0; i < SENSOR_COUNT; i++) {
    revs[i].prevTime = 0;
    pinMode(revs[i].port, INPUT);
  }
  Serial.begin(9600);   
}

void loop() {
  for (i = 0; i < SENSOR_COUNT; i++) {
    revs[i].value = digitalRead(revs[i].port);
    if (revs[i].value == 1 && revs[i].prevValue == 0) {
      revs[i].nowTime = micros();
      if (revs[i].prevTime > 0) {  
        revs[i].diff = revs[i].nowTime - revs[i].prevTime;
        revs[i].revs = (float) 1000000 / (4 * revs[i].diff);
        Serial.println(String(String(i) + ":" + String(revs[i].revs, 3)));
      }
      revs[i].prevTime = revs[i].nowTime;
    }
    revs[i].prevValue = revs[i].value;
  }
}
