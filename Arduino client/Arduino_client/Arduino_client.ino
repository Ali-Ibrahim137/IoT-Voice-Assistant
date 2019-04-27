#include <SPI.h>
#include <ESP8266WiFi.h>
#include <ThingerESP8266.h>
#include <DHT.h>

#define USERNAME "Karam_dar25"
#define DEVICE_ID "greenhouse"
#define DEVICE_CREDENTIAL "greenhouse"

#define SSID "Karam_D-Link"
#define SSID_PASSWORD "264961711#"

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
  
  thing["light"] << [](pson & in) {
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

  thing["qw"] << [](pson & in) {
    bool f = in["qw"];
    if(f==1)waterRelayState = HIGH;
    else waterRelayState = LOW;
    digitalWrite(WaterRelayPin, waterRelayState);
  };
  
  thing["water"] = []() {
    if(autoMode==0){
      double SoilMoistureSensorValue = map(analogRead(SoilMoistureSensorPin), 0, 1023, 0, 100);
      if(SoilMoistureSensorValue>80){         // 80% or some other value, will put it after testing
        waterRelayState = HIGH;
        digitalWrite(WaterRelayPin, waterRelayState);
      }
      while(1){
        SoilMoistureSensorValue = map(analogRead(SoilMoistureSensorPin), 0, 1023, 0, 100);
        if(SoilMoistureSensorValue<65){         // 40% or some other value, will put it after testing
          waterRelayState = LOW;
          digitalWrite(WaterRelayPin, waterRelayState);
          break;
        }
      }
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
    waterRelayState=LOW;
    digitalWrite(WaterRelayPin, waterRelayState);
    ledState=LOW;
    digitalWrite(LedPin, ledState);
    autoMode = 0;
  };
}

void loop() {
  if(autoMode==1){
    double SoilMoistureSensorValue = map(analogRead(SoilMoistureSensorPin), 0, 1023, 0, 100);
      if(SoilMoistureSensorValue>80){         // 40% or some other value, will put it after testing
       waterRelayState = HIGH;
       digitalWrite(WaterRelayPin, waterRelayState);
     }
     while(1){
      SoilMoistureSensorValue = map(analogRead(SoilMoistureSensorPin), 0, 1023, 0, 100);
      if(SoilMoistureSensorValue<65){         // 40% or some other value, will put it after testing
        waterRelayState = LOW;
        digitalWrite(WaterRelayPin, waterRelayState);
        break;
      }
    }
  }      
  thing.handle();
}
