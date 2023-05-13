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
