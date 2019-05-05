#include <SPI.h>
#include <ESP8266WiFi.h>
#include <ThingerESP8266.h>
#include <DHT.h>

#define USERNAME "Karam_dar25"
#define DEVICE_ID "greenhouse"
#define DEVICE_CREDENTIAL "greenhouse"

#define SSID "****"
#define SSID_PASSWORD "****"

ThingerESP8266 thing (USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);


const int WaterRelayPin = 12; 			//D6
const int LedPin = 4; 				//D2

const int SoilMoistureSensorPin = 14; 		//D5
const int DhtSensorPin = 13; 			//D3

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
  pinMode(SoilMoistureSensorPin, INPUT);
  
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
      bool SoilMoistureSensorValue = digitalRead(SoilMoistureSensorPin);
      if(digitalRead(SoilMoistureSensorPin)==HIGH){
        waterRelayState = HIGH;
        digitalWrite(WaterRelayPin, waterRelayState);
        while(digitalRead(SoilMoistureSensorPin)==HIGH){
          ESP.wdtFeed();
          SoilMoistureSensorValue = digitalRead(SoilMoistureSensorPin);
        }
      }
      waterRelayState = LOW;
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
    out["moisture"] = digitalRead(SoilMoistureSensorPin);
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
      bool SoilMoistureSensorValue = digitalRead(SoilMoistureSensorPin);
      if(digitalRead(SoilMoistureSensorPin)==HIGH){
        waterRelayState = HIGH;
        digitalWrite(WaterRelayPin, waterRelayState);
        while(digitalRead(SoilMoistureSensorPin)==HIGH){
          ESP.wdtFeed();
          SoilMoistureSensorValue = digitalRead(SoilMoistureSensorPin);
        }
      }
      waterRelayState = LOW;
      digitalWrite(WaterRelayPin, waterRelayState);       
    }
  thing.handle();
} 
