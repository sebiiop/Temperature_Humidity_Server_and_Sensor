#include <ESP8266WiFi.h>
#include <ESP8266Ping.h>
#include <Wire.h>
#include <WiFiUdp.h>


String board_id = "arduino1";
int deep_sleep_time_in_minutes = 5;

float temp_offset = -1.00; //offset value for temperature
float hum_offset = -6.00; //offset value for humidity
float calibration = -1.62; // Check Battery voltage using multimeter & add/subtract the value

// Set up the server IP address and port
//const char* SERVER = "192.168.1.119";
//const int PORT = 1234;

//waits for ip adress of the server
WiFiUDP udp;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
IPAddress serverIP;
const int PORT = 1234;



const char* ssid_list[] = {"Modem", "A1-Mesh-WLAN-953c8", "WLAN17919585"};
const char* password_list[] = {"katzenklokatzenklo", "23238218744460743715", "ns6ruvRmjudF"};

const int num_networks = sizeof(ssid_list) / sizeof(ssid_list[0]);
int current_network = 0;
boolean wifi_connected = false;


//WiFiClient client;
WiFiServer server(80);

// Define a function to send data to the server
bool send_data(String board_id, float celsTemp, float humidity, float voltage, float bat_percentage) {
  // Connect to the server
  WiFiClient client;
  if (!client.connect(serverIP, PORT)) {
    //delete the server ip address
    serverIP = IPAddress();
    Serial.println("Failed to connect to the server. ServerIP deleted.");
    return false;
  }

  // Send the data with the ID
  String message = "ID: " + String(board_id) + ", Temperature: " + String(celsTemp) + ", Humidity: " + String(humidity) + ", Voltage; " + String(voltage) +", Battery_percentage: " + String(bat_percentage);
  Serial.println(message);
  client.print(message);

  // Wait for a response from the server
  while (!client.available()) {
    delay(10);
  }

  // Read the response from the server
  String response = client.readString();
  Serial.println(response);

  // Close the connection
  client.stop();
  return true;
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {
  // Seed the random number generator
  randomSeed(analogRead(0));
  Serial.begin(9600);

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

  //ping to receive a ip address from the router
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
  
  udp.begin(1234); // Port to listen for UDP messages
  
  Serial.println("Waiting for IP address");
}

void loop() {
  
  if (serverIP == IPAddress()) {
    int packetSize = udp.parsePacket();
    if (packetSize) {
      IPAddress remoteIP = udp.remoteIP();
      udp.read((char*)&serverIP, sizeof(serverIP));
      Serial.print("Received UDP message from ");
      Serial.println(remoteIP);
      Serial.print("Server IP: ");
      Serial.println(remoteIP);

      udp.beginPacket(remoteIP, 1234); // Port to send the response
      udp.write("IP received");
      udp.endPacket();
      Serial.println("Sent response to the server");

      serverIP = remoteIP;
      //Serial.println("Server address is " + serverIP);
    
    }
    
  }
  else {
    // Perform operations assuming the ESP8266 is connected to the server
    // Generate random values for temperature, humidity, voltage, and battery percentage
  float celsTemp = random(0, 100);
  float humidity = random(0, 100);
  float voltage = random(0, 5);
  int bat_percentage = random(0, 100);
  
  // Output the values
  Serial.print("Temperature (C): ");
  Serial.println(celsTemp);
  
  Serial.print("Humidity (%): ");
  Serial.println(humidity);
  
  Serial.print("Voltage (V): ");
  Serial.println(voltage);
  
  Serial.print("Battery Percentage (%): ");
  Serial.println(bat_percentage);
  
  delay(1000);  // Wait for a second
  



  // Send the data to the server and wait for a response
  if (send_data(board_id, celsTemp, humidity, voltage, bat_percentage)) {
    // If the response was received, put the ESP8266 into deep sleep for 9 minutes
    Serial.println("Going to sleep");
    //ESP.deepSleep(9 * 60 * 1000 * 1000);
  } else {
    // If the response was not received, wait for 5 seconds before retrying
    delay(5000);
  }


      

  
  delay(1000);
  Serial.println("Waking up");

}
}
