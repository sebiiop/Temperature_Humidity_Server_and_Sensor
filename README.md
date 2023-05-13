# Temperature_Humidity_Server_and_Sensor
The temp_hum_server.py starts a flask application which displays a graph and provides a link to download all the available data in a csv file. Furthermore, 
it coordinates the request_esp8266 application.
The request_exp8266.py script first looks for the ip address of the router.
Afterwards it uses this ip adress to ping all devices in the network using nmap.
This is necessary to get a working arp -a list where the esp modules are inculded.

The ip address is then sent to the available esp8266 boards, which in return start sending data back to the server. After sending, the go into deep sleep
for 9 minutes.

The data is saved by the server in a csv file and a graph is generated, which is displayed by the flask app.



For installation please install the temp_hum_esp8266 file on a esp8266 equipped with a SI7021 sensor. Calibrate the sensor with the offset values temp_offset, hum_offset and battery_calibration.


On the server, pull the github repository and use the install.sh script for linux. A crontab can be setup with the setup_cronjob.sh file.
This will install all the necessary dependencies and create a cronjob, which starts the process automatically.



In the wiring and stl folders, 3d models and grbl files for cnc cutting can be found. They are of course optional.



# Installation:

-Esp8266
Install the temp_hum_esp8266.ino file. Then measure the temperature, humidity and voltage with external equipment and compare  them to the Serial.print outputs in the arduino IDE.
Adjust the compansation values for temperature, humidity and voltage in the IDE and reinstall the file to the esp8266.

Please be aware that the reset pin has to be disconnected to install the script and reconnected for the script to work properly. Check here the wiring diagramm, provided in the folder
wiring.

-Raspberry Pi server
Install git with:
    "sudo apt-get install git"
  
  Afterwards git clone the repository.

Then setup the crontab jobs with:
    "bash Temperature_Humidity_Server_and_Sensor/setup_cronjob.sh"
Please be aware here, that a cronjob file has to be implemented already. Check with 
    "crontab -e"

To start the installation script, use:
    "sudo bash Temperature_Humidity_Server_and_Sensor/install.sh"
This will install the remaining dependencies and restart the Raspberry Pi once it is finished.


After that the Pi will start to send it´s IP address to the Esp8266 and start collecting data from them.

The server page can be accessed by <ip_raspberry_pi:4200>.
