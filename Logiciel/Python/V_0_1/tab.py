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

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ThingSpeak Data</title>
    <style>
        .chart-row {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            padding: 10px 0;
        }
        iframe {
            margin-bottom: 5px; 
        }
        .tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
        }
        .tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
        }
        .tab button:hover {
            background-color: #ddd;
        }
        .tab button.active {
            background-color: #ccc;
        }
        .tabcontent {
            display: none;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-top: none;
        }
        #nightModeButton {
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 5px;
            cursor: pointer;
        }
    </style>
    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        function toggleNightMode() {
            var body = document.body;
            body.classList.toggle("night-mode");
            var button = document.getElementById("nightModeButton");
            if (body.classList.contains("night-mode")) {
                button.textContent = "Light Mode";
                body.style.backgroundColor = "#333";
                body.style.color = "#fff";
            } else {
                button.textContent = "Night Mode";
                body.style.backgroundColor = "#fff";
                body.style.color = "#000";
            }
        }

        function fetchData() {
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temperature1').textContent = data.Temperature1;
                    document.getElementById('temperature2').textContent = data.Temperature2;
                    document.getElementById('temperature3').textContent = data.Temperature3;
                    document.getElementById('temperature4').textContent = data.Temperature4;
                    document.getElementById('temperatureAtlas').textContent = data.TemperatureAtlas;
                    document.getElementById('co2').textContent = data.CO2;
                    document.getElementById('humidity').textContent = data.Humidity;
                })
                .catch(error => console.error('Error fetching data:', error));
        }

        setInterval(fetchData, 2000);  // Fetch data every 2 seconds
        window.onload = function() {
            openTab(event, 'Dashboard'); // Open the 'Tableau de bord' tab by default
        };
    </script>
</head>
<body>
    <button id="nightModeButton" onclick="toggleNightMode()">Night Mode</button>
    <h1>Test Sherbrooke</h1>
    <div class="tab">
        <button class="tablinks" onclick="openTab(event, 'Dashboard')">Tableau de bord</button>
        <button class="tablinks" onclick="openTab(event, 'Control')">Contrôle</button>
        <button class="tablinks" onclick="openTab(event, 'Download')">Télécharger</button>
    </div>
    <div id="Control" class="tabcontent">
        <form action="/action/chauffage" method="post" target="log">
            <input type="submit" value="Chauffage">
        </form>
        <form action="/action/ventilation" method="post" target="log">
            <input type="submit" value="Ventilation">
        </form>
        <form action="/action/lumiere" method="post" target="log">
            <input type="submit" value="Lumière">
        </form>
        <form action="/action/deshumidificateurs" method="post" target="log">
            <input type="submit" value="Déshumidificateurs">
        </form>
        <form action="/action/flex" method="post">
            <input type="submit" value="Flex">
        </form>
        <form method="post">
            <label for="setTemp">Control Temp1:</label>
            <input type="text" id="setTemp" name="setTemp" value="{{ input_temp }}">
            <input type="submit" value="Set">
            <input type="submit" name="clear" value="Clear">
        </form>
        <div>Set Temperature: <span id="setTemperature">{{ set_temp_display }}</span></div>
        <div>Temperature1: <span id="temperature1">Loading...</span></div>
        <div>Temperature2: <span id="temperature2">Loading...</span></div>
        <div>Temperature3: <span id="temperature3">Loading...</span></div>
        <div>Temperature4: <span id="temperature4">Loading...</span></div>
        <div>TemperatureAtlas: <span id="temperatureAtlas">Loading...</span></div>
        <div>CO2: <span id="co2">Loading...</span></div>
        <div>Humidity: <span id="humidity">Loading...</span></div>
    </div>
    <div id="Dashboard" class="tabcontent">
        <div class="chart-row">
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=20&title=Temp%C3%A9rature+D1&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=50&yaxismin=5"></iframe>
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/widgets/421466"></iframe>
        </div>  
        <div class="chart-row">
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D2&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5"></iframe>
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/widgets/421467"></iframe>
        </div>
        <div class="chart-row">
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D3&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5"></iframe>
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/widgets/421468"></iframe>
        </div>
        <div class="chart-row">
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/charts/4?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D4&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5"></iframe>
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/widgets/421469"></iframe>
        </div>
        <div class="chart-row">
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/charts/6?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=CO%C2%B2&type=line&xaxis=Time&yaxis=PPM&yaxismax=1000&yaxismin=0"></iframe>
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/widgets/421472"></iframe>
        </div>
        <div class="chart-row">
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/charts/7?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Humidit%C3%A9&type=line&xaxis=Time&yaxis=%25&yaxismax=100&yaxismin=0"></iframe>
            <iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1296899/widgets/421471"></iframe>       
        </div>
    </div>
    <div id="Download" class="tabcontent">
        <h1>Data 30 jours</h1>
        <button onclick="window.location.href = '/download/json'">Download JSON</button>
        <button onclick="window.location.href = '/download/xml'">Download XML</button>
        <button onclick="window.location.href = '/download/csv'">Download CSV</button> 
    </div>
</body>
</html>
""", set_temp_display=set_temp_display, input_temp=input_temp)

@app.route('/download/json')
def download_json():
    response = requests.get(f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?days=30&api_key={READ_API_KEY}")
    if response.ok:
        return Response(
            response.content,
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment;filename=data.json'}
        )
    else:
        return "Failed to fetch data", 500

@app.route('/download/xml')
def download_xml():
    response = requests.get(f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.xml?days=30&api_key={READ_API_KEY}")
    if response.ok:
        return Response(
            response.content,
            mimetype='application/xml',
            headers={'Content-Disposition': 'attachment;filename=data.xml'}
        )
    else:
        return "Failed to fetch data", 500

@app.route('/download/csv')
def download_csv():
    response = requests.get(f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?days=30&api_key={READ_API_KEY}")
    if response.ok:
        return Response(
            response.content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=data.csv'}
        )
    else:
        return "Failed to fetch data", 500


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

@app.route('/action/ventilation', methods=['POST'])
def ventilation():
    # Remplacer l'URL ci-dessous par l'URL de votre appareil
    url = "http://10.42.0.88/cm?cmnd=Power%20toggle"
    try:
        response = requests.get(url)
        return f"Chauffage commuté. Status: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la commutation du chauffage: {e}"
    return "Ventilation contrôlée."

@app.route('/action/lumiere', methods=['POST'])
def lumiere():
    url = "http://10.42.0.130/cm?cmnd=Power%20toggle"
    url1 = "http://10.42.0.29/cm?cmnd=Power%20toggle"
    
    try:
        response = requests.get(url)
        response = requests.get(url1)
        return f"Lumière commuté. Status: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la commutation du Lumière: {e}"
   
@app.route('/action/deshumidificateurs', methods=['POST'])
def deshumidificateurs():
    url = "http://10.42.0.85/cm?cmnd=Power%20toggle"
    try:
        response = requests.get(url)
        return f"deshumidificateurs commuté. Status: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la commutation du deshumidificateurs: {e}"
    return "Déshumidificateurs contrôlés."

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
