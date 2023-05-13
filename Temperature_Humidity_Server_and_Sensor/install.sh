#!/bin/bash

#install dependencies
apt-get update -y
apt-get upgrade -y
apt-get autoremove -y
apt-get install python3-pip -y
apt-get install nmap -y
apt-get install python3-numpy -y
apt-get install python3-matplotlib -y
apt-get install python3-pandas -y



path=$(pwd)

pip3 install -r ${path}/Temperature_Humidity_Server_and_Sensor/requirements.txt


file1="${path}/Temperature_Humidity_Server_and_Sensor/src/temp_hum_server.py"
file2="${path}/Temperature_Humidity_Server_and_Sensor/src/request_esp8266.py"
file3="${path}/Temperature_Humidity_Server_and_Sensor/src/send_ip_to_esp8266.py"
file4="${path}/Temperature_Humidity_Server_and_Sensor/src/dynamic_df_plot.py"

chmod +x ${file1}
chmod +x ${file2}
chmod +x ${file3}
chmod +x ${file4}


reboot now