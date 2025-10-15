#include <Wire.h>
#include "Adafruit_DRV2605.h" //Driver Lib
#include <Adafruit_CircuitPlayground.h> //Controller Lib

Adafruit_DRV2605 drv;

void setup() {
  Serial.begin(115200);
  CircuitPlayground.begin();
  drv.begin();
  drv.selectLibrary(1);
  drv.setMode(DRV2605_MODE_INTTRIG);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    if (cmd.startsWith("VIB")) {
      int intensity = cmd.substring(3).toInt();
      
      // Haptic Effects
      drv.setWaveform(0, 47);
      drv.setWaveform(1, 0);
      drv.go();
      
      // LED Effects
      int brightness = map(intensity, 0, 255, 0, 255);
      for (int i = 0; i < 10; i++) {
        CircuitPlayground.setPixelColor(i, brightness, 0, brightness); //can change the color
      }
      delay(100);
      CircuitPlayground.clearPixels();
    }
  }
}