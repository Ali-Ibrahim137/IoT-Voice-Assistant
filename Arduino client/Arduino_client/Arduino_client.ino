#include <SPI.h>
#include <ESP8266WiFi.h>
#include <ThingerESP8266.h>
#include <DHT.h>

#define USERNAME "New_Horizons"
#define DEVICE_ID "greenhouse"
#define DEVICE_CREDENTIAL "greenhouse"

#define SSID "ACM LAB"
#define SSID_PASSWORD "acm14acm"

ThingerESP8266 thing (USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);


const int WaterRelayPin = 5;
const int LedPin = 4;

const int SoilMoistureSensorPin = 17;
const int DhtSensorPin = 0;

const int DhtType = DHT22;

int ledState = LOW;
int waterRelayState = LOW;
int autoMode = 0;

DHT dht(DhtSensorPin, DhtType);

void setup() {
  Serial.begin(9600);
  dht.begin();
  thing.add_wifi(SSID, SSID_PASSWORD);
  pinMode(WaterRelayPin, OUTPUT);
  pinMode(LedPin, OUTPUT); 
  pinMode(LED_BUILTIN, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  
  thing["led"] << [](pson & in) {
    if(autoMode==0){
      bool f = in["value"];
      if(f==1)ledState=HIGH;
      else ledState=LOW;
      digitalWrite(LedPin, ledState);
    }
  };


  thing["auto"] << [](pson & in) {
    bool f = in["value"];
    autoMode = f;
  };
  
  thing["water"] << [](pson & in) {
    if(autoMode==0){
      bool f = in["value"];
      if(f==1)waterRelayState=HIGH;
      else waterRelayState=LOW;
      digitalWrite(WaterRelayPin, waterRelayState);
    }
  };
  
  
  thing["temperature"] >> [](pson & out) {
    out["celsius"] = dht.readTemperature();
  };
  thing["humidity"] >> [](pson & out) {
    out["humidity"] = dht.readHumidity();
  };

  thing["moisture"] >> [](pson & out) {
    out["moisture"] = map(analogRead(SoilMoistureSensorPin), 0, 1023, 0, 100);
  };
  thing["reset"] = [](){
    waterRelayState=HIGH;
    ledState=HIGH;
    autoMode = 0;
  };
}

void loop() {
  if(autoMode==1){
    while(1){
      int temp = dht.readTemperature();
      if(temp<25){
        ledState = HIGH;
        break;
      }
      digitalWrite(LedPin, LOW);
      delay(100);
      digitalWrite(LedPin, HIGH);
      delay(200);
      continue;
      double SoilMoistureSensorValue = map(analogRead(SoilMoistureSensorPin), 0, 1023, 0, 100);
      if(SoilMoistureSensorValue>40){         // 40% or someother value, will put it after testing
        waterRelayState = HIGH;
        digitalWrite(WaterRelayPin, waterRelayState);
        break;
      }
    }
  }
  thing.handle();
}
