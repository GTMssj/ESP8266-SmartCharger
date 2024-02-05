#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define SSID "CMCC-"
#define PSWD "5f2m2ey3"
IPAddress local_IP(192,168,1,8);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

WiFiUDP Udp;

unsigned int localUdpPort = 4444;

int packetSize;

void setup() {
  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);
  Serial.begin(115200);
  Serial.println();
  WiFi.mode(WIFI_STA);
  if (!WiFi.config(local_IP, gateway, subnet)){
    Serial.println("STA Fail");
  }
  WiFi.begin(SSID, PSWD);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.print(WiFi.localIP());
  Serial.printf(" on port %d\n", localUdpPort);
  digitalWrite(2, HIGH);
  Udp.begin(localUdpPort);
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
