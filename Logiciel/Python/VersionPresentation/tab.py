'''
    @file       tab.py
    @date       Avril 2024
    @version    0.1
                Interface web.
    @brief      Ce fichier comprend le page web
                Il récupère les valeurs critiques pour la gestion des boucles de contrôle.
                Gestion de la communication avec les prises intelligentes via le point d'accès WIFI.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
'''
from flask import Flask, render_template_string, jsonify, request, Response ,redirect
import requests
import json
import xml.etree.ElementTree as ET
import csv
import threading
import time
import os

app = Flask(__name__)

CHANNEL_ID = "1296899"
READ_API_KEY = "M15BVTOEBCFHQL7K"
DEVICE_URL = "http://10.42.0.88/cm?cmnd=Power%20"
lock = threading.Lock()
last_command = [None]  
set_temp_file = "set_temp.txt"  

def get_thing_speak_data():
    base_url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
    params = {
        'results': 1,
        'api_key': READ_API_KEY,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        feeds = data['feeds'][0]
        return {
            'Temperature1': feeds['field1'],
            'Temperature2': feeds['field2'],
            'Temperature3': feeds['field3'],
            'Temperature4': feeds['field4'],
            'TemperatureAtlas': feeds['field5'],
            'CO2': feeds['field6'],
            'Humidity': feeds['field7'],
        }
    else:
        return {}

def save_set_temperature(temp):
    with open(set_temp_file, 'w') as file:
        file.write(str(temp))

def get_saved_set_temperature():
    if os.path.exists(set_temp_file):
        with open(set_temp_file, 'r') as file:
            return file.read().strip()
    return "NA"

def control_temperature(temp1, set_temp, last_command):
    try:
        temp1 = float(temp1)
        set_temp = float(set_temp)
    except ValueError:
        return

    if temp1 > set_temp + 0.5 and last_command[0] != "off":
        requests.get(f"{DEVICE_URL}off")
        last_command[0] = "off"
    elif temp1 < set_temp - 0.5 and last_command[0] != "on":
        requests.get(f"{DEVICE_URL}On")
        last_command[0] = "on"


@app.route('/', methods=['GET', 'POST'])
def index():
    set_temp_display = get_saved_set_temperature()
    input_temp = "" 

    if request.method == 'POST':
        with lock:
            if 'setTemp' in request.form and request.form['setTemp']:
                set_temp = request.form['setTemp']
                save_set_temperature(set_temp)
                set_temp_display = set_temp  
                input_temp = ""
            elif 'clear' in request.form:
                save_set_temperature('NA')
                set_temp_display = "NA"  
                last_command[0] = None

    return render_template_string

@app.route('/')
def home():
return render_template_string(HTML)

@app.route('/action/chauffage', methods=['POST'])
def chauffage():
# Remplacer l'URL ci-dessous par l'URL de votre appareil
url = "http://10.42.0.23/cm?cmnd=Power%20toggle"
try:
    response = requests.get(url)
    
    
    return f"Chauffage commuté. Status: {response.status_code}"
except Exception as e:
    return f"Erreur lors de la commutation du chauffage: {e}"


@app.route('/action/flex', methods=['POST'])
def flex():
url3 = "http://10.42.0.85/cm?cmnd=Power%20toggle"
url2 = "http://10.42.0.130/cm?cmnd=Power%20toggle"
url1 = "http://10.42.0.29/cm?cmnd=Power%20toggle"
url = "http://10.42.0.88/cm?cmnd=Power%20toggle"
try:
    for x in range(2):
        response = requests.get(url)
        time.sleep(0.1)
        response = requests.get(url1)
        time.sleep(0.1)
        response = requests.get(url2)
        time.sleep(0.1)
        response = requests.get(url3)
        time.sleep(0.1)
        
    response = requests.get(url)
    response = requests.get(url2)
    
    for x in range(2):
        
        response = requests.get(url)
        response = requests.get(url2)
        response = requests.get(url1)
        response = requests.get(url3)
        time.sleep(0.5)
        
    response = requests.get(url)
    response = requests.get(url2)
    return f"!!!!! . Status: {response.status_code}"
except Exception as e:
    return f"Erreur : {e}"
return "flex contrôlés."

@app.route('/data')
def data():
return jsonify(get_thing_speak_data())

def temperature_control_loop():
while True:
    with lock:
        data = get_thing_speak_data()
        set_temp = get_saved_set_temperature()
        if data and set_temp != "NA":
            control_temperature(data['Temperature1'], set_temp, last_command)
    time.sleep(1) 

if __name__ == '__main__':
control_thread = threading.Thread(target=temperature_control_loop)
control_thread.daemon = True
control_thread.start()
app.run(host='0.0.0.0', port=80)
