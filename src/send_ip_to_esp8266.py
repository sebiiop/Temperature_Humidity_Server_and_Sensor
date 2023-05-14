import requests
import time
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import socket


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

    device_ip = []

    #ping all ip adresses in network
    os.popen(f"nmap -sn {home_ip_network}")
    os.system(f'nmap -sn {home_ip_network}')
    time.sleep(10)

    #look for the arduino ip adresses

    for device in os.popen('arp -a'):
        print("Step 2 - Find the client IP addresses\n\n") 
        print(device)
        device = str(device)
        device = device.replace("[","")
        device = device.replace("]","")
        device = device.replace("(","")
        device = device.replace(")","")
        device = " ".join(device.split())
        device = device.replace(" ",",")
        print(device)
        device = device.split(",")
        print(device)
        
        #find the ip address in the string
        device = [i for i in device if home_submask_ip in i]
        print(device)
    

    
        device_ip.append(device[0])
    

    device_ip = [x for x in device_ip if '.' in x]
 

    print("Step 3 - send IP address to esp8266\n\n")
    print(device_ip)

    # to remove duplicated from list 
    ip_result = [] 
    [ip_result.append(x) for x in device_ip if x not in ip_result] 

    print("\n\nAddresses to ping\n\n")
    print(ip_result)

    for ip in ip_result:
        print(ip)
        UDP_IP = ip  # Replace with the IP address of your ESP8266
        UDP_PORT = 1234  # Replace with the UDP port number used in your ESP8266 script
        BUFFER_SIZE = 1024
        MESSAGE = home_ip_network

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout of x seconds
        sock.settimeout(1)

        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        print(f"Sent IP address to ESP: {ip}")

        try:
            # Wait for a response from the ESP8266
            data, addr = sock.recvfrom(BUFFER_SIZE)
            response = data.decode()
            print("Received response from ESP:", response)
        except socket.timeout:
            print("No response received from ESP within 1 seconds")

        # Close the socket
        sock.close()

working_directory = os.getcwd()
os.chdir(working_directory)

home_ip_network, home_submask_ip = find_home_ip()
device_names = request_data(home_ip_network, home_submask_ip)