#include <WiFi.h>
#include "DHT.h"
#include "ThingSpeak.h"

#define DHTPIN 21
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Wokwi-GUEST";
const char* password = "";

WiFiClient client;

unsigned long myChannelNumber = 3007093;
const char* myWriteAPIKey = "COLVAM760BJNLE33";

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
  ThingSpeak.begin(client);
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    delay(10000);
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C  | Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);

  int statusCode = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

  if (statusCode == 200) {
    Serial.println("Channel update successful.");
  } else {
    Serial.print("Problem updating channel. HTTP error code ");
    Serial.println(statusCode);
  }

  delay(20000);
}
