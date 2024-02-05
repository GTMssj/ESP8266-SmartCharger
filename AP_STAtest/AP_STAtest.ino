#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

WiFiUDP Udp;

IPAddress apip(192,168,2,1);
IPAddress apgateway(192,168,2,1);
IPAddress apmsk(255,255,255,0);

IPAddress staip(192,168,1,8);
IPAddress stagateway(192,168,1,1);
IPAddress stamsk(255,255,255,0);

unsigned int localPort = 4444;
unsigned int remotePort = 4444;

const char* SSID = "CMCC-";
const char* PASSWD = "5f2m2ey3";
const char* apSSID = "ESP8266-Charger";
const char* apPASSWD = "12345679";

int packetSize;

void setup() {
  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);
  Serial.begin(115200);
  Serial.println();
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAPConfig(apip, apgateway, apmsk);
  WiFi.softAP(apSSID, apPASSWD, 1);
  WiFi.config(staip, stagateway, stamsk);
  WiFi.begin(SSID, PASSWD);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.println();
  Serial.println("Connected!");
  Serial.print("IP address: ");
  Serial.print(WiFi.localIP());
  Serial.print(" on port ");
  Serial.println(localPort);
  Serial.print("AP address: ");
  Serial.print(WiFi.softAPIP());
  Serial.print(" on port ");
  Serial.println(remotePort);
  digitalWrite(2, HIGH);
  Udp.begin(localPort);
}

void loop() {
  packetSize = Udp.parsePacket();
  if (packetSize) {
    byte InPacket[packetSize];
    Udp.read(InPacket, packetSize);
    switch(InPacket[0]){
      case 0b00000000:
        digitalWrite(2, LOW);
        digitalWrite(0, LOW);
        Serial.println("ON");
        break;
      case 0b00000001:
        digitalWrite(0, HIGH);
        digitalWrite(2, HIGH);
        Serial.println("OFF");
        break;
    }
  }
}