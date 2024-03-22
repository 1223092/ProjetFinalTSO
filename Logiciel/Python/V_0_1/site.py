'''
    @file       site.py
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
  

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">                             
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Serrebrooke</title>
        <style>
            .chart-row 
            {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;    
            }                            
            .control-button 
            {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 20px;
                background-color: #333;
                border-radius: 20px;
                color: white;
                font-size: 1.2em;
                box-shadow: inset 0 0 10px #000;
            }
            .input-value 
            {
                width: 20%; 
                padding: 10px; 
                margin: 5px 0; 
                box-sizing: border-box; 
            }                      
            .control-button span 
            {
                margin-right: 10px;
            }                      
            .control-button:hover
            {
                background-color: #444;
            }
            .control-icon 
            {
                font-size: 1.5em;
            }
            .control-status 
            {
                margin-left: auto;
            }                      
            #title 
            {
                font-size: 3em; 
                color: #fff; 
                background: -webkit-linear-gradient(#007d35, #005322); 
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin: 20px 0;
                font-family: 'Arial', sans-serif; 
                text-shadow: 2px 2px 4px #000; 
            }
            .control-panel 
            {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;                  
                margin-top: 40px; 
            }                        
            
            .download-buttons 
            {     
                display: flex; 
                justify-content: center; 
                margin-top: 20px;                            
            } 
                     
            body.night-mode .control-button 
            {
                background-color: #222; 
                box-shadow: inset 0 0 10px #fff; 
            }
        </style>
    
</head>
<body>
    <div class="container mt-4">
        <button id="nightModeButton" onclick="toggleNightMode()" class="btn btn-dark mb-4">Dark Mode</button>
        <h1 id="title" class="text-center mb-4">Serrebrooke</h1>
        <ul class="nav nav-tabs" id="myTab" role="tablist">       
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="dashboard-tab" data-bs-toggle="tab" data-bs-target="#Dashboard" type="button" role="tab" aria-controls="Dashboard" aria-selected="true">Tableau de bord</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="control-tab" data-bs-toggle="tab" data-bs-target="#Control" type="button" role="tab" aria-controls="Control" aria-selected="false">Contrôle</button>
            </li>  
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="programming-tab" data-bs-toggle="tab" data-bs-target="#Programming" type="button" role="tab" aria-controls="Programming" aria-selected="false">Programmation</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="download-tab" data-bs-toggle="tab" data-bs-target="#Download" type="button" role="tab" aria-controls="Download" aria-selected="false">Télécharger</button>
            </li>
        </ul> 
         
        <div class="tab-content" id="myTabContent">                          
            <div class="tab-pane fade" id="Control" role="tabpanel" aria-labelledby="control-tab">
                <div class="control-panel">
                    <!-- Humidificateur -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.85', 'deshumidificateursState', 'action/deshumidificateurs')">
                        <span class="control-icon">💧</span>
                        Humidificateur:  <span id="deshumidificateursState" class="control-status"></span>
                    </div>

                    <!-- Chauffage -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.23', 'chauffageState', 'action/chauffage')">
                        <span class="control-icon">🔥</span>
                        Chauffage: <span id="chauffageState" class="control-status"></span>                
                    </div>

                    <!-- Lumière 1 -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.130', 'lumiere1State', 'action/lumiere1')">
                        <span class="control-icon">💡</span>
                        Lumière 1: <span id="lumiere1State" class="control-status"></span>
                    </div>

                    <!-- Lumière 2 -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.29', 'lumiere2State', 'action/lumiere2')">
                        <span class="control-icon">💡</span>
                        Lumière 2: <span id="lumiere2State" class="control-status"></span>
                    </div>

                    <!-- Ventilation -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.88', 'ventilationState', 'action/ventilation')">
                        <span class="control-icon">🌀</span>
                        Ventilation: <span id="ventilationState" class="control-status"></span>
                    </div>
                </div>                      
            </div>

            <div class="tab-pane fade" id="Download" role="tabpanel" aria-labelledby="download-tab">
                <h2>Download Data: 30 jours</h1>
                <div class="download-buttons">
                    <button onclick="window.location.href = '/download/json'" class="btn btn-primary m-2 ">Download JSON</button>
                    <button onclick="window.location.href = '/download/xml'" class="btn btn-primary m-2">Download XML</button>
                    <button onclick="window.location.href = '/download/csv'" class="btn btn-primary m-2">Download CSV</button>
                </div>
            </div>                    
            <div class="tab-pane fade" id="Programming" role="tabpanel" aria-labelledby="programming-tab">
                <ul class="nav nav-tabs" id="innerTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="fixed-values-tab" data-bs-toggle="tab" data-bs-target="#FixedValues" type="button" role="tab" aria-controls="FixedValues" aria-selected="true">Valeurs Fixes</button>
                    </li>
                </ul>
                <div class="tab-content" id="innerTabContent">
                    <div class="tab-pane fade show active" id="FixedValues" role="tabpanel" aria-labelledby="fixed-values-tab">                  
                        <div class="temperature-set-section">
                            <h2>Définir la valeur de température</h2>
                            <input type="number" id="temperatureValue" class="input-value" placeholder="Entrez la température en Celsius" step="0.01">
                            <button onclick="setTemperature()">Définir</button>
                            <button onclick="clearTemperature()">Effacer</button>
                            <p>Température actuelle définie : <span id="currentTemperature">NA</span>°C</p>
                        </div> 
                        <div class="humidity-set-section">
                            <h2>Définir la valeur d'humidité</h2>
                            <input type="number" id="humidityValue" class="input-value" placeholder="Entrez l'humidité en pourcentage" min="0" max="100" step="0.01">
                            <button onclick="setHumidity()">Définir</button>
                            <button onclick="clearHumidity()">Effacer</button>
                            <p>Humidité actuelle définie : <span id="currentHumidity">NA</span>%</p>
                        </div>           
                    </div>               
                </div>                                                                                                                        
            </div>                      
            <div class="tab-pane fade show active" id="Dashboard" role="tabpanel" aria-labelledby="dashboard-tab">
                <div class="row">
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=20&title=Temp%C3%A9rature+D1&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=50&yaxismin=5" allowfullscreen></iframe>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/widgets/421466" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D2&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5" allowfullscreen></iframe>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/widgets/421467" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D3&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5" allowfullscreen></iframe>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/widgets/421468" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/4?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D4&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5" allowfullscreen></iframe>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/widgets/421469" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/6?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=CO%C2%B2&type=line&xaxis=Time&yaxis=PPM&yaxismax=1000&yaxismin=0" allowfullscreen></iframe>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/widgets/421472" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/7?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Humidit%C3%A9&type=line&xaxis=Time&yaxis=%25&yaxismax=100&yaxismin=0" allowfullscreen></iframe>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/widgets/421471" allowfullscreen></iframe>
                    </div>
                </div>
            </div>                                                  
        </div>
    </div>
    <script>
        function setHumidity() {
            var humidity = document.getElementById('humidityValue').value;
            fetch('/set_humidity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ humidity: humidity }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('currentHumidity').textContent = humidity;
            })
            .catch(error => console.error('Erreur:', error));
        }

        function clearHumidity() {
            fetch('/clear_humidity', {
                method: 'POST',
            })
            .then(response => {
                document.getElementById('currentHumidity').textContent = 'NA';
                document.getElementById('humidityValue').value = '';
            })
            .catch(error => console.error('Erreur:', error));
        }

        function fetchCurrentHumidity() {
            fetch('/get_current_humidity')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('currentHumidity').textContent = data.humidity || 'NA';
                })
                .catch(error => console.error('Erreur:', error));
        }

        document.getElementById('programming-tab').addEventListener('click', fetchCurrentHumidity);

        function fetchCurrentTemperature() {
            fetch('/get_current_temperature')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('currentTemperature').textContent = data.temperature || 'NA';
                })
                .catch(error => console.error('Erreur:', error));
        }

        // Appeler fetchCurrentTemperature lorsque l'onglet Programmation est sélectionné
        document.getElementById('programming-tab').addEventListener('click', fetchCurrentTemperature);                          
        function setTemperature() {
            var temperature = document.getElementById('temperatureValue').value;
            fetch('/set_temperature', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ temperature: temperature }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('currentTemperature').textContent = temperature;
            })
            .catch(error => console.error('Erreur:', error));
        }

        function clearTemperature() {
            fetch('/clear_temperature', {
                method: 'POST',
            })
            .then(response => {
                document.getElementById('currentTemperature').textContent = 'NA';
                document.getElementById('temperatureValue').value = '';
            })
            .catch(error => console.error('Erreur:', error));
        }
                                                    
        function openTab(evt, tabName) 
        {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) 
                {
                    tabcontent[i].style.display = "none";
                }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) 
            {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        function toggleNightMode() 
            {
            var body = document.body;
            body.classList.toggle("night-mode");
            var button = document.getElementById("nightModeButton");
            if (body.classList.contains("night-mode")) 
            {
                button.textContent = "Light Mode";
                body.style.backgroundColor = "#333";
                body.style.color = "#fff";
            } 
            else 
            {
                button.textContent = "Night Mode";
                body.style.backgroundColor = "#fff";
                body.style.color = "#000";
            }
        }
        function toggleDeviceState(ip, elementId, actionRoute) 
        {
            
            fetch(`/${actionRoute}`, 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ip: ip })
            })
            .then(response => response.json())
            .then(data => {
                
                document.getElementById(elementId).textContent = data.state;
            })
            .catch(error => console.error('Error:', error));
        }

        window.onload = function() 
        {
            openTab(event, 'Dashboard'); 
        };
    
            function fetchState(ip, elementId) 
            {
                fetch(`/state/${ip}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById(elementId).textContent = data.state;
                    })
                    .catch(error => console.error('Error:', error));
            }

        function updateStates() 
        {
            fetchState('10.42.0.23', 'chauffageState');
            fetchState('10.42.0.88', 'ventilationState');
            fetchState('10.42.0.130', 'lumiere1State');
            fetchState('10.42.0.29', 'lumiere2State');
            fetchState('10.42.0.85', 'deshumidificateursState');
        }
        setInterval(updateStates, 1000);  
    </script>                                                              
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>                                 
</body>
</html>
""", )


@app.route('/state/<ip>')
def state(ip):
    url = f"http://{ip}/cm?cmnd=Power"
    try:
        response = requests.get(url)
        state = response.json().get('POWER')
        return jsonify({'state': state})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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


@app.route('/get_current_temperature')
def get_current_temperature():
    try:
        with open('temp_set.txt', 'r') as file:
            temperature = file.read().strip()
            if not temperature:  # Si le fichier est vide, renvoyer "NA"
                temperature = "NA"
    except FileNotFoundError:
        temperature = "NA"  # Si le fichier n'existe pas, renvoyer "NA"
    return jsonify({'temperature': temperature})

@app.route('/set_temperature', methods=['POST'])
def set_temperature():
    data = request.get_json()
    temperature = data.get('temperature')
    with open('temp_set.txt', 'w') as file:
        file.write(temperature)
    return jsonify({'status': 'success'})

@app.route('/clear_temperature', methods=['POST'])
def clear_temperature():
    open('temp_set.txt', 'w').close()
    return jsonify({'status': 'success'})

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



@app.route('/action/chauffage', methods=['POST'])
def chauffage():
    
    data = request.get_json()
    ip = data.get('ip')
    url = f"http://{ip}/cm?cmnd=Power%20toggle"
    try:
        response = requests.get(url)       
        newState = response.json().get('POWER')
        return jsonify({'state': newState})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/action/ventilation', methods=['POST'])
def ventilation():
    
    url = "http://10.42.0.88/cm?cmnd=Power%20toggle"
    try:
        response = requests.get(url)
        return f"Chauffage commuté. Status: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la commutation du chauffage: {e}"
   

@app.route('/action/lumiere1', methods=['POST'])
def lumiere1():
    url = "http://10.42.0.130/cm?cmnd=Power%20toggle"
       
    try:
        response = requests.get(url)
       
        return f"Lumière commuté. Status: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la commutation du Lumière: {e}"
 
@app.route('/action/lumiere2', methods=['POST'])
def lumiere2():
    
    url = "http://10.42.0.29/cm?cmnd=Power%20toggle"
    
    try:
        response = requests.get(url)
        
        return f"Lumière commuté. Status: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la commutation du Lumière: {e}"
 
 
@app.route('/action/deshumidificateurs', methods=['POST'])
def deshumidificateurs():
    url = "http://{ip}/cm?cmnd=Power/cm?cmnd=Power%20toggle"
    try:
        response = requests.get(url)
        return f"deshumidificateurs commuté. Status: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la commutation du deshumidificateurs: {e}"
   
@app.route('/set_humidity', methods=['POST'])
def set_humidity():
    data = request.get_json()
    humidity = data.get('humidity')
    with open('hum_set.txt', 'w') as file:
        file.write(humidity)
    return jsonify({'status': 'success'})

@app.route('/clear_humidity', methods=['POST'])
def clear_humidity():
    open('hum_set.txt', 'w').close()
    return jsonify({'status': 'success'})

@app.route('/get_current_humidity')
def get_current_humidity():
    try:
        with open('hum_set.txt', 'r') as file:
            humidity = file.read().strip()
            if not humidity:  # Si le fichier est vide, renvoyer "NA"
                humidity = "NA"
    except FileNotFoundError:
        humidity = "NA"  # Si le fichier n'existe pas, renvoyer "NA"
    return jsonify({'humidity': humidity})

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
