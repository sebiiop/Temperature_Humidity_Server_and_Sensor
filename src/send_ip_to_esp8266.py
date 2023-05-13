import requests
import time
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import socket
from datetime import datetime
import sys
import subprocess


def find_home_ip():
    #find the ip adress of the router and format the ip to use in nmap
    #home_ip = str(os.system("hostname -I"))
    #home_ip = socket.gethostbyname(socket.gethostname())
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    home_ip = s.getsockname()[0]
    s.close()

    print(home_ip)
    print(home_ip.split("."))

    part_one, part_two, part_three, part_four = home_ip.split(".")

    home_ip_network = [part_one, part_two, part_three, "*"]
    home_submask_ip = [part_one, part_two, part_three]

    s = "."

    home_ip_network = s.join(home_ip_network)
    home_submask_ip = s.join(home_submask_ip)
    print(home_ip_network)
    print(home_submask_ip)

    return home_ip_network, home_submask_ip


def request_data(home_ip_network, home_submask_ip):
    current_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())
    print(current_time)

    print("Step 1 - Scan the home network for clients\n\n")

    

    try:
        #ping all ip adresses in network
        os.popen(f"nmap -sn {home_ip_network}")
        os.system(f'nmap -sn {home_ip_network}')
        time.sleep(1)

    except Exception as e:
        print(e)

    ip_result =[]
    #ping through all possible ip addresses
    for i in range(1,256):
        ip = f"{home_submask_ip}.{i}"
        ip_result.append(ip)

    for ip in ip_result:
        print(ip)
        UDP_IP = ip  # Replace with the IP address of your ESP8266
        UDP_PORT = 1234  # Replace with the UDP port number used in your ESP8266 script
        BUFFER_SIZE = 1024
        MESSAGE = home_ip_network

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout of x seconds
        sock.settimeout(0.5)

        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        print(f"Sent IP address to ESP: {ip}")

        try:
            # Wait for a response from the ESP8266
            data, addr = sock.recvfrom(BUFFER_SIZE)
            response = data.decode()
            print("Received response from ESP:", response)
        except socket.timeout:
            print("No response received from ESP within 0.5 seconds")

        # Close the socket
        sock.close()

    

#Timestamp for log
now = datetime.now()
print(now)

#Set the working directory for the script
working_directory = os.getcwd()
if working_directory.endswith("src"):
    os.chdir(working_directory)
    print(f"The current working directory is:\n{working_directory}\n\n")
else:
    working_directory = os.path.join(os.getcwd(), "Temperature_Humidity_Server_and_Sensor","src")
    print(f"The current working directory is:\n{working_directory}\n\n")
    os.chdir(working_directory)

home_ip_network, home_submask_ip = find_home_ip()
device_names = request_data(home_ip_network, home_submask_ip)