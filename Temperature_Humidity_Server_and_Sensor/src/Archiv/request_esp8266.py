import requests
import time
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import socket

device_names = []


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


def request_data(home_ip_network, device_names, home_submask_ip):
    current_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())
    print(current_time)

    print("Step 1\n\n")

    #device_ip = ["10.0.0.13","10.0.0.15", "10.0.0.89"]
    device_ip = []

    #ping all ip adresses in network
    os.popen(f"nmap -sn {home_ip_network}")
    os.system(f'nmap -sn {home_ip_network}')
    time.sleep(10)

    #look for the arduino ip adresses

    for device in os.popen('arp -a'):
        print("Step 2\n\n") 
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
 

    print("Step 3\n\n")
    print(device_ip)


    for ip in device_ip:
        print(ip)
        try:
            ip = f"http://{ip}/sensor"
            print("Step 4\n\n")
            print(f"\nRequest to {ip}\n")
            response = requests.get(f"{ip}", timeout=10)
            response = response.text
            response = response.strip("\n")
            response = response.strip("\r")
            print(response)

            if "arduino" in response:
                print("Step 5\n\n")
                print(ip)
                print(response)
                board_id, temperature, humidity, voltage, charge = response.split(",")
                print(board_id)
                print(temperature)
                print(humidity)
                print(voltage)
                print(charge)
                row= []
                row.append(current_time)
                #row.append(board_id)
                row.append(temperature)
                row.append(humidity)
                row.append(voltage)
                row.append(charge)

                with open(f"{board_id}.csv", "a", newline="") as csv_file:
                    # Create CSV writer
                    writer = csv.writer(csv_file, delimiter=",")

                    
                    writer.writerow(row)

                if board_id not in device_names:
                    device_names.append(board_id)


                #send sleep command
                time.sleep(2)
                print("sending arduino to sleep")
                requests.get(f"http://{ip}/sleep",timeout=5)


        except Exception as e:
            #print("e")
            pass
    
    return device_names

def create_summarized_csv(device_names):
    print("Step 6")
    print(device_names)
    # Read the CSV files
    df1 = pd.read_csv(f'{device_names[0]}.csv')
    df2 = pd.read_csv(f'{device_names[1]}.csv')
    df3 = pd.read_csv(f'{device_names[2]}.csv')

#df = [df1, df2, df3]
    df = pd.concat([df1, df2, df3], axis=1)
    df.columns =['timestamp', 'arduino1_temperature', 'arduino1_humidity', 'arduino1_voltage', 'arduino1_charge', "arduino2_timestamp", 'arduino2_temperature', 'arduino2_humidity',  'arduino2_voltage', 'arduino2_charge',"arduino3_timestamp", 'arduino3_temperature', 'arduino3_humidity', 'arduino3_voltage', 'arduino3_charge']
    df = df.drop('arduino2_timestamp', axis=1)
    df = df.drop('arduino3_timestamp', axis=1)

    print(df)

    # saving the dataframe
    df.to_csv('data.csv')

def create_graph_from_csv(device_names):
    number_of_measurement_points = 50
    print("Step 7")
    print(device_names)

    # Read the CSV files
    df1 = pd.read_csv(f'{device_names[0]}.csv')
    df1.columns =['timestamp', 'temperature', 'humidity', 'voltage', 'charge']
    if len(df1)>number_of_measurement_points:
        df1 = df1.tail(number_of_measurement_points)
    df2 = pd.read_csv(f'{device_names[1]}.csv')
    df2.columns =['timestamp', 'temperature', 'humidity', 'voltage', 'charge']
    if len(df2)>number_of_measurement_points:
        df2 = df2.tail(number_of_measurement_points)
    df3 = pd.read_csv(f'{device_names[2]}.csv')
    df3.columns =['timestamp', 'temperature', 'humidity', 'voltage', 'charge']
    if len(df3)>number_of_measurement_points:
        df3 = df3.tail(number_of_measurement_points)

    # Create a new figure with 3 subplots
    fig, axs = plt.subplots(nrows=3, ncols=1, sharex=True)

    # Plot the temperature and humidity data for each CSV file
    axs[0].plot(df1['timestamp'], df1['temperature'], '-', label='Temperature')
    axs[0].plot(df1['timestamp'], df1['humidity'], '-', label='Humidity')
    axs[1].plot(df2['timestamp'], df2['temperature'], '-', label='Temperature')
    axs[1].plot(df2['timestamp'], df2['humidity'], '-', label='Humidity')
    axs[2].plot(df3['timestamp'], df3['temperature'], '-', label='Temperature')
    axs[2].plot(df3['timestamp'], df3['humidity'], '-', label='Humidity')

    # Add a title and labels to the x-axis and y-axes
    fig.suptitle('Temperature and Humidity')
    axs[0].set_xlabel(f'Timestamp\nVoltage: {df1.voltage.tail(1)}\nCharge: {df1.charge.tail(1)}')
    axs[0].set_ylabel('Temperature (°C)')
    axs[1].set_xlabel(f'Timestamp\nVoltage: {df2.voltage.tail(1)}\nCharge: {df2.charge.tail(1)}')
    axs[1].set_ylabel('Temperature (°C)')
    axs[2].set_xlabel(f'Timestamp\nVoltage: {df3.voltage.tail(1)}\nCharge: {df3.charge.tail(1)}')
    axs[2].set_ylabel('Temperature (°C)')

    # Add a legend to the big plot
    fig.legend(loc='upper right')  

    plt.tight_layout()

    

    # Save the figure as a JPEG file
    path = os.getcwd()
    path_static = os.path.join(path, "static")
    file_path_static = os.path.join(path_static, "image.jpg")
    fig.savefig(file_path_static)


home_ip_network, home_submask_ip = find_home_ip()
device_names = request_data(home_ip_network, device_names, home_submask_ip)
#create_summarized_csv(device_names)
#create_graph_from_csv(device_names)