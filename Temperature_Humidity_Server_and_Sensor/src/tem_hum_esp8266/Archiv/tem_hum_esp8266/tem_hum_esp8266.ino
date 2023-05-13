#include <ESP8266WiFi.h>
#include <ESP8266Ping.h>
#include <Wire.h>


String board_id = "arduino2";
int deep_sleep_time_in_minutes = 9;

float temp_offset = -2.70; //offset value for temperature
float hum_offset = 11.80; //offset value for humidity
float calibration = -3.80; // Check Battery voltage using multimeter & add/subtract the value

// Set up the server IP address and port
const char* SERVER = "your_server_ip_address";
const int PORT = 1234;





// SI7021 I2C address is 0x40(64)
#define si7021Addr 0x40

const char* ssid_list[] = {"Modem", "A1-Mesh-WLAN-953c8", "WLAN17919585"};
const char* password_list[] = {"katzenklokatzenklo", "23238218744460743715", "ns6ruvRmjudF"};

const int num_networks = sizeof(ssid_list) / sizeof(ssid_list[0]);
int current_network = 0;
boolean wifi_connected = false;

bool sent_message = false;


//WiFiClient client;
WiFiServer server(80);




void setup() {

  //initialize wire connection to SI70 sensor
  Wire.begin();
  Serial.begin(9600);
  delay(10);
  Wire.beginTransmission(si7021Addr);
  Wire.endTransmission();
  delay(300);

  // Connect to WiFi network
  while (current_network < num_networks && !wifi_connected) {
    Serial.printf("Connecting to WiFi network %s...\n", ssid_list[current_network]);
    WiFi.begin(ssid_list[current_network], password_list[current_network]);

    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 20) {
      delay(500);
      Serial.print(".");
      retries++;
    }

    if (WiFi.status() == WL_CONNECTED) {
      wifi_connected = true;
      Serial.printf("\nConnected to %s with IP address %s\n", ssid_list[current_network], WiFi.localIP().toString().c_str());
    } else {
      Serial.printf("\nFailed to connect to %s\n", ssid_list[current_network]);
      current_network++;
    }
  }

  if (!wifi_connected) {
    Serial.println("Unable to connect to any networks!");
  }

  // Start the server
  server.begin();
  Serial.println("Server started");




}

void loop() {
    if (sent_message) {
    Serial.println("Going to sleep");
    ESP.deepSleep(60e6 * deep_sleep_time_in_minutes); 
    Serial.println("Waking up");

    // Restart Arduino 
    ESP.restart();
   }

  const IPAddress remote_ip(8, 8, 8, 8);
  Serial.print("");
  Serial.print("");
  Serial.print("Pinging ip ");
  Serial.println(remote_ip);
  
  if(Ping.ping(remote_ip)) {
    Serial.println("Success!!");
  } else {
    Serial.println("Error :(");
  }


  
  //read sensor data
  //add a 22k ohm resistor and a 47k ohm resistor. take the voltage between the two and connect to a0
  int analogInPin  = A0;    // Analog input pin
  int sensorValue;          // Analog Output of Sensor
  int bat_percentage;

  sensorValue = analogRead(analogInPin);
  float voltage = (((sensorValue * 3.3) / 1024) * 2 + calibration); //multiply by two as voltage divider network is 100K & 100K Resistor
 
  bat_percentage = mapfloat(voltage, 2.8, 4.2, 0, 100); //2.8V as Battery Cut off Voltage & 4.2V as Maximum Voltage
 
  if (bat_percentage >= 100)
  {
    bat_percentage = 100;
  }
  if (bat_percentage <= 0)
  {
    bat_percentage = 1;
  }
 
  Serial.print("Analog Value = ");
  Serial.print(sensorValue);
  Serial.print("\t Output Voltage = ");
  Serial.print(voltage);
  Serial.print("\t Battery Percentage = ");
  Serial.println(bat_percentage);



  

  //delay(10000);



  
  unsigned int data[2];
 
  Wire.beginTransmission(si7021Addr);
  //Send humidity measurement command
  Wire.write(0xF5);
  Wire.endTransmission();
  delay(500);
 
  // Request 2 bytes of data
  Wire.requestFrom(si7021Addr, 2);
  // Read 2 bytes of data to get humidity
  if(Wire.available() == 2)
  {
    data[0] = Wire.read();
    data[1] = Wire.read();
  }
 
  // Convert the data
  float humidity  = ((data[0] * 256.0) + data[1]);
  humidity = ((125 * humidity) / 65536.0) + hum_offset;
 
  Wire.beginTransmission(si7021Addr);
  // Send temperature measurement command
  Wire.write(0xF3);
  Wire.endTransmission();
  delay(500);
 
  // Request 2 bytes of data
  Wire.requestFrom(si7021Addr, 2);
 
  // Read 2 bytes of data for temperature
  if(Wire.available() == 2)
  {
    data[0] = Wire.read();
    data[1] = Wire.read();
  }
 
  // Convert the data
  float temp  = ((data[0] * 256.0) + data[1]);
  float celsTemp = ((175.72 * temp) / 65536.0) - 46.85 + temp_offset;

  // Output data to serial monitor
  Serial.print("Humidity : ");
  Serial.print(humidity);
  Serial.println(" % RH");
  Serial.print("Celsius : ");
  Serial.print(celsTemp);
  Serial.println(" C");
  
  
  delay(1000);



  
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }

  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();


   if (request.indexOf("/sensor") != -1) {
    // Send data to Python script with Arduino identifier
    String answer_data = String(board_id) + "," + String(celsTemp) + "," + String(humidity) + "," + String(voltage) + "," + String(bat_percentage);
    Serial.println(answer_data);
    Serial.println(celsTemp);
    //client.println(celsTemp);
   
  

    // Return the response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/plain");
    //client.println("Connection: close");  // the connection will be closed after completion of the response
    client.println();
    client.println(answer_data);
    delay(1000);

    sent_message = true;
    //Serial.println("Client disonnected");
    }
   
  // Disconnect from server
  //client.stop();

  

}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
