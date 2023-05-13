import time
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
from datetime import datetime

def create_summarized_csv(device_names):
    print("Step 6")

    #create empty dataframe
    df = {}
    
    print(device_names)

    for i in range(len(device_names)):
        #save df_id to df_list
        df_id = f"df{i}"

        #create headers for summarized dataframe
        df_columns =[]
        df_columns.append(f"{device_names[i]}_timestamp")
        df_columns.append(f"{device_names[i]}_temperature")
        df_columns.append(f"{device_names[i]}_humidity")
        df_columns.append(f"{device_names[i]}_voltage")
        df_columns.append(f"{device_names[i]}_battery_percentage")

        print(df_columns)

        df_test = pd.DataFrame(columns=df_columns)
        df_test = pd.read_csv(f'{device_names[i]}.csv')
        print(df_test)

        #add the dataframe to the dictionary
        df[df_id] = pd.read_csv(f'{device_names[i]}.csv', names=df_columns)


    
    print(df)

    summarized_df = pd.concat(df.values(), axis = 1)
    print(summarized_df)


    # saving the dataframe
    summarized_df.to_csv('data.csv')
    

def create_graph_from_csv(device_names):
    number_of_measurement_points = 50
    subplots_adjust(hspace=0.000)
    number_of_subplots=len(device_names)


    if number_of_subplots < 2:
        df = pd.read_csv(f"{device_names[-1]}.csv")
        df.columns =['timestamp', 'temperature', 'humidity', 'voltage', 'charge']
        plt.plot(df['timestamp'], df['temperature'], label='Temperature')
        plt.plot(df['timestamp'], df['humidity'], label='Humidity')
        plt.plot(df['timestamp'], df['charge'], label='Charge')

        plt.legend()

        # Save the figure as a JPEG file
        path = os.getcwd()
        path_static = os.path.join(path, "static")
        file_path_static = os.path.join(path_static, "image.jpg")
        # Save the plot as a JPG file
        plt.savefig(file_path_static)


    else:
        fig, axs = plt.subplots(nrows=number_of_subplots, ncols=1, sharex=True)

        #create subplots according to device_names
        for i,v in enumerate(range(number_of_subplots)):

            #read from csv and save the last x-values
            df = pd.read_csv(f"{device_names[v-1]}.csv")
            df.columns =['timestamp', 'temperature', 'humidity', 'voltage', 'charge']
            if len(df)>number_of_measurement_points:
                df = df.tail(number_of_measurement_points)

            #create the subplots
            v = v+1
            axs[v-2] = subplot(number_of_subplots,1,v)
            #ax1.plot(x,y)
            axs[v-2].plot(df['timestamp'], df['temperature'], '-', label='Temperature')
            axs[v-2].plot(df['timestamp'], df['humidity'], '-', label='Humidity')
            axs[v-2].plot(df['timestamp'], df['charge'], '-', label='Battery_charge')


        # Add a legend to the big plot
        fig.legend(loc='upper right')  

        plt.tight_layout()

        #plt.show()

        # Save the figure as a JPEG file
        path = os.getcwd()
        path_static = os.path.join(path, "static")
        file_path_static = os.path.join(path_static, "image.jpg")
        fig.savefig(file_path_static)


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




device_names = []
csv_files = [f for f in os.listdir(working_directory) if f.endswith('.csv')]
search_string = "arduino"
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




