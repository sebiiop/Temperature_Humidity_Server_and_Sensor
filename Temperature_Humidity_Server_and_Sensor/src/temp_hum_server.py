from flask import Flask, render_template, send_file
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
import random
## importing socket module
import socket
from datetime import datetime


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

app = Flask(__name__, static_url_path = "/static", static_folder = "static")
scheduler = BackgroundScheduler()

def run_script():
    #print("Running request script...")
    return render_template('index.html')
    

scheduler.add_job(run_script, 'interval', minutes=1)
scheduler.start()

@atexit.register
def shutdown():
    scheduler.shutdown()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download():
    return send_file('data.csv', mimetype='text/csv')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
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

    print("Running request script...")
    # Your script code goes here
    #os.popen('python3 request_esp8266.py')
    
    port = 5000 + random.randint(0, 999)
    print(port)

    app.run(host = ip_address, port="4200", debug=False, threaded=False)