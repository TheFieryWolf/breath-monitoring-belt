#include <ArduinoBLE.h>

int sensorPinA = A0;
int sensorPinB = A1;
int sensorPinC = A2;
int sensorPinD = A3; 

float timer;
float nowTime;
float lastTime;
float vals[4];


// #define BLE_UUID_VOLTAGE1_CHAR "00002a19-0000-1000-8000-00805f9b34fb"
#define BLE_UUID_VOLTAGES_CHAR "00002a19-0000-1000-8000-00805f9b34fc"

// // Define the BLE service and characteristics

BLEService voltagesService("VoltagesService");
BLECharacteristic voltagesCharacteristic(BLE_UUID_VOLTAGES_CHAR, BLERead | BLENotify,20); // remote clients will only be able to read this float

void setup() {
  Serial.begin(115200);
  // Initialize BLE
  BLE.begin();
  BLE.setLocalName("Will's_Will");

  BLE.setAdvertisedService(voltagesService);
  voltagesService.addCharacteristic(voltagesCharacteristic);
  BLE.addService(voltagesService);

  // Start advertising
  BLE.advertise();
  Serial.println("Bluetooth device active, waiting for connections...");

}


void loop() {
  BLEDevice central = BLE.central();
  // struct vals values;
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
  }
  lastTime = 0;
  timer = 0;
  while (central.connected()) {
    nowTime = millis();
    timer = timer + (nowTime - lastTime)/1000.0;
    lastTime = nowTime;

    vals[0] = timer;
    vals[1] = (analogRead(sensorPinA) / 1023.0) * 3.3;
    vals[2] = (analogRead(sensorPinB) / 1023.0) * 3.3; 
    vals[3] = (analogRead(sensorPinC) / 1023.0) * 3.3;
    vals[4] = (analogRead(sensorPinD) / 1023.0) * 3.3;

    Serial.print("Time:  ");
    Serial.print(timer);
    Serial.print("  A:  ");
    Serial.print(vals[1]);
    Serial.print("  B:  ");
    Serial.print(vals[2]);
    Serial.print("  C:  ");
    Serial.print(vals[3]);
    Serial.print("  D:  ");
    Serial.println(vals[4]);

    // Write the characteristic value (immediately notifies, unlike setValue())
    voltagesCharacteristic.writeValue(vals,20);
    delay(50);
  }
}
