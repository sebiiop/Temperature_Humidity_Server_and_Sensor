
import socket
import threading
import csv
import os
import json
from datetime import datetime

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

# Define the host and port to listen on
HOST = '0.0.0.0'
PORT = 1234

# Initialize a dictionary to store the data from each device
device_data = {}

# Create a lock to prevent multiple threads from writing to the same file
file_lock = threading.Lock()

# Define a function to handle incoming client connections
def handle_client(conn, addr):
    print('Connected by', addr)

    # Receive the data from the client
    data = conn.recv(1024).decode()
    if not data:
        print('No data received')
        conn.close()
        return

    # Parse the data into values
    try:
        print(data)
        board_id, temp, humidity, voltage, bat_percentage = data.split(",")
        board_id = board_id.split(" ")[-1]
        print(board_id)
        temp = temp.split(" ")[-1]
        print(temp)
        humidity = humidity.split(" ")[-1]
        print(humidity)
        voltage = voltage.split(" ")[-1]
        print(voltage)
        bat_percentage = bat_percentage.split(" ")[-1]
        print(bat_percentage)
        
        # Send response to client indicating data has been received
        response = {"status": "success", "message": "Data received"}
        conn.sendall(json.dumps(response).encode())


    except ValueError:
        print('Invalid data received:', data)
        conn.close()
        return

    # Determine the device ID based on the client address
    device_id = addr[0]

    filename = f"{board_id}.csv"
    print(filename)
    
    # If this is the first time we've received data from this device, create a new CSV file to store the data
    if os.path.isfile(filename) == False:

        
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([f"{board_id}_timestamp", f"{board_id}_temperature", f"{board_id}_humidity", f"{board_id}_voltage", f"{board_id}_charge"])
        print(f'Created new file {filename}')

    #get current datetime
    dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Print the device_data
    print("device_data")
    print(board_id, dt, temp, humidity, voltage, bat_percentage)

    # Write the data to the device's CSV file
    #filename = f'{device_id}.csv'
    with file_lock:
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([dt, temp, humidity, voltage, bat_percentage])

    # Close the connection to the client
    conn.close()
    print('Connection closed')
    print("\n\n")

# Define a function to start the server
def start_server():
    # Create a TCP socket and bind it to the host and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f'Server listening on {HOST}:{PORT}')
    print("\n\n")

    # Start accepting incoming client connections
    while True:
        try:
            conn, addr = sock.accept()
        except KeyboardInterrupt:
            print('Server stopped')
            return
        except Exception as e:
            print(f'Error accepting connection: {e}')
            continue

        # Spawn a new thread to handle the client connection
        threading.Thread(target=handle_client, args=(conn, addr)).start()


## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip_address = s.getsockname()[0]
s.close()



#ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")


# Start the server
start_server()
