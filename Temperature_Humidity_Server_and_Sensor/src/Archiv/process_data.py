import time
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt



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


    
    #Change the subplot logic to a dynamic one
    #https://stackoverflow.com/questions/12319796/dynamically-add-create-subplots-in-matplotlib




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





search_string = "arduino"
working_directory = os.getcwd()
csv_files = [f for f in os.listdir(working_directory) if f.endswith('.csv')]


device_names = []
for csv_file in csv_files:
    if search_string in csv_file:
        print(f"{csv_file} contains {search_string}")
        csv_file = csv_file.split(".")[0]
        device_names.append(csv_file)


print("5")
for i in range(len(device_names)):
    df = pd.read_csv(f"{device_names[i]}.csv")
    #checking the number of empty rows in th csv file
    print (df.isnull().sum())
    #Droping the empty rows
    modifiedDF = df.dropna()
    #Saving it to the csv file 
    modifiedDF.to_csv(f"{device_names[i]}.csv",index=False)

create_summarized_csv(device_names)
create_graph_from_csv(device_names)
