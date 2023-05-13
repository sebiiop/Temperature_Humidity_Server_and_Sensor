#!/bin/bash



path=$(pwd)

file1="${path}/Temperature_Humidity_Server_and_Sensor/src/temp_hum_server.py"
file2="${path}/Temperature_Humidity_Server_and_Sensor/src/request_esp8266.py"
file3="${path}/Temperature_Humidity_Server_and_Sensor/src/send_ip_to_esp8266.py"
file4="${path}/Temperature_Humidity_Server_and_Sensor/src/dynamic_df_plot.py"

#setup crontab
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo " "  >> mycron
echo "#Temperature_Humidity_Server_and_Sensor" >> mycron
echo "@reboot sleep 20 && /usr/bin/python3 ${file1}  >> /home/pi/server_log.txt" >> mycron
echo "@reboot sleep 30 && /usr/bin/python3 ${file2}  >> /home/pi/request_log.txt" >> mycron
echo "*/2 * * * * /usr/bin/python3 ${file3}  >> /home/pi/send_ip_log.txt" >> mycron
echo "*/2 * * * * /usr/bin/python3 ${file4}  >> /home/pi/dynamic_df_plot.txt" >> mycron

sleep 2

echo "Adding cron tasks"

sleep 2

echo "Install new cron file"

sleep 2

crontab mycron

echo "Finished adding cron tasks"

sleep 2

rm mycron


