'''
    @file       site_final.py
    @date       Mai 2024
    @version    0.1
                
    @brief      Fichier contentant tout les parties du site de contrôle.
                Les styles css utilisé.
                Toute la strucutre html.
                Les méthodes pour intéragir avec le systèmes.
    
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python     
'''
#Librairies Python
from flask import Flask, render_template_string, jsonify, request, Response ,redirect
import requests
import json
import xml.etree.ElementTree as ET


app = Flask(__name__)
#SETTINGS_FILE = 'control_settings.json'
SETTINGS_FILE = '/root/app-serrebrooke/control_settings.json'
CHANNEL_ID = "1296899"
READ_API_KEY = "M15BVTOEBCFHQL7K"

HEATER_IP = "10.42.0.23"
VENTILATION_IP = "10.42.0.88"
LUMIERE_IP = "10.42.0.130"
HUMIDIFICATEUR_IP = "10.42.0.85"

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

        .time-input {
            width: 250px; 
        }                              
                                
        .tooltip {
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted black;                      
            cursor: pointer; 
            opacity: 1;                                        
        }

        .state-icon {
            padding-left: 10px;
        }
                          
                                  
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 140px;
            background-color: black;
            color: white;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1000;                                       
            left: 100%;   
            margin-left: 70px;                      
        }

        .tooltip:hover .tooltiptext {
            visibility: visible ;
        }                   
                                                                        
        .schedule-section div, .timer-section div {
            margin-bottom: 10px;
        }

        input[type="number"], input[type="time"], select {
            margin-right: 10px;
            margin-bottom: 5px;
        }
                    
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
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="settings-tab" data-bs-toggle="tab" data-bs-target="#Settings" type="button" role="tab" aria-controls="Settings" aria-selected="false">Paramètres</button>
            </li>                      
        </ul> 
         
        <div class="tab-content" id="myTabContent">                          
            <div class="tab-pane fade" id="Control" role="tabpanel" aria-labelledby="control-tab">
                <div class="control-panel">

                    <!-- Chauffage -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.23', 'chauffageState', 'action/chauffage')">
                        <span class="control-icon">🔥</span>
                        Chauffage: <span id="chauffageState" class="control-status"></span>                
                    </div>

                    <!-- Lumière  -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.130', 'lumiere1State', 'action/lumiere1')">
                        <span class="control-icon">💡</span>
                        Lumière : <span id="lumiere1State" class="control-status"></span>
                    </div>
             
                    <!-- Ventilation -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.88', 'ventilationState', 'action/ventilation')">
                        <span class="control-icon">🌀</span>
                        Ventilation: <span id="ventilationState" class="control-status"></span>
                    </div>
                    <!-- Déshumidificateur -->
                    <div class="control-button" onclick="toggleDeviceState('10.42.0.85', 'deshumidificateurState', 'action/deshumidificateur')">
                        <span class="control-icon">💧</span>
                        Humidificateur: <span id="deshumidificateurState" class="control-status"></span>                
                    </div>              
                </div>                      
            </div>
            <div class="tab-pane fade" id="Settings" role="tabpanel" aria-labelledby="settings-tab">
                
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
                <div class="container">
                    <!-- Température Section -->                  
                    <div class="section-frame"> 
                        <button class="btn btn-success" onclick="saveSettings()">Sauvegarde</button>                
                        <h2>Chauffage<span id="chauffageIcon" class="state-icon">🔴</span></h2>
                        <label for="tempDeadband">Bande morte de température:</label>
                        <input type="number" id="tempDeadband" class="input-value form-control" placeholder="Température en °C">                                
                        <h4>Température (Moyenne: <span id="averageTemperature">Loading...</span>°C)</h4>    
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activerTemp" onchange="toggleTemperatureSection(this.checked);">
                            <label class="form-check-label" for="activerTemp">Activer</label>
                            <div class="tooltip">?
                                <span class="tooltiptext">Activer ou désactiver le point de consigne hors horaire.</span>
                            </div>      
                        </div>
                        <label for="temperatureValue">Point de consigne Chauffage:</label>
                        <input type="number" id="temperatureValue" class="input-value form-control" placeholder="Entrez la température en Celsius" step="1.0" disabled>
                                 
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activerSecondTemp" onchange="toggleSecondTemperatureSection(this.checked);" >
                            <label class="form-check-label" for="activerSecondTemp">Activer Chauffage</label>
                            <div class="tooltip">?
                                <span class="tooltiptext">Activer ou désactiver le point de consigne pour la plage horaire choisi.</span>
                            </div>       
                        </div>
                        <label for="secondTemperatureValue">Point de consigne Chauffage:</label>
                        <input type="number" id="secondTemperatureValue" class="input-value form-control" placeholder="Entrez une autre température en Celsius" step="1.0" disabled>
                        <label for="chauffageStartTime">Heure de démarrage Chauffage:</label>
                        <input type="time" id="heatingStartTime" class="form-control time-input" disabled>
                        <label for="chauffageEndTime">Heure de fin Chauffage:</label>
                        <input type="time" id="heatingEndTime" class="form-control time-input" disabled>
                    </div>
                    
                    <!-- Ventilation Section -->
                    <div class="section-frame">
                        <h2>Ventilation<span id="ventilationIcon" class="state-icon">🔴</span></h2>
                        <label for="ventDeadband">Bande morte de ventilation:</label>
                        <input type="number" id="ventDeadband" class="input-value form-control" placeholder="Humidité en %">          
                        <h4>Humidité (Dernière: <span id="latestHumidity">Loading...</span>%)</h4>             
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activerHumidity" onchange="toggleHumidityControl(this.checked);">
                            <label class="form-check-label" for="activerHumidity">Activer</label>
                            <span class="tooltip">?
                                <span class="tooltiptext">Activer ou désactiver le point de consigne hors horaire.</span>
                            </span>
                        </div>
                        <label for="humidityValue">Point de consigne Humidité:</label>          
                        <input type="number" id="humidityValue" class="input-value form-control" placeholder="Humidité (%)" min="0" max="100" disabled>                      
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activerVent" onchange="toggleVentilationControl(this.checked);">
                            <label class="form-check-label" for="activerVent">Activer Contrôles</label>
                            <span class="tooltip">?
                                <span class="tooltiptext">Activer ou désactiver le point de consigne pour la plage horaire choisi.</span>
                            </span>                    
                        </div>
                        <label for="humidityValue2">Point de consigne Humidité:</label>
                        <input type="number" id="humidityValue2" class="input-value form-control" placeholder="Humidité (%)" min="0" max="100" disabled >          
                        <label for="ventilationStartTime">Heure de démarrage Ventilation:</label>
                        <input type="time" id="ventilationStartTime" class="form-control time-input" disabled>
                        <label for="ventilationEndTime">Heure de fin Ventilation:</label>
                        <input type="time" id="ventilationEndTime" class="form-control time-input" disabled>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activateTimer" onchange="toggleTimerControl(this.checked);">
                            <label class="form-check-label" for="activateTimer">Activer Mode Timer</label>
                        </div>
                        <label for="timerOn">Temps ON (secondes):</label>
                        <input type="number" id="timerOn" class="input-value form-control" placeholder="Temps ON en secondes" disabled>
                        
                        <label for="timerOff">Temps OFF (minutes):</label>
                        <input type="number" id="timerOff" class="input-value form-control" placeholder="Temps OFF en minutes" disabled>
                                            
                    </div>                 
                    <!-- Humidificateur Section -->
                    <div class="section-frame">
                        <h2>Humidificateur<span id="humidificateurIcon" class="state-icon">🔴</span></h2>
                        <label for="humDeadband">Bande morte d'humidité:</label>
                        <input type="number" id="humDeadband" class="input-value form-control" placeholder="Humidité en %">          
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activateHumidificateur" onchange="toggleHumidificateurSection(this.checked);">
                            <label class="form-check-label" for="activateHumidificateur">Activer</label>
                        </div>
                        <label for="humidificateurValue">Point de consigne Humidité:</label>
                        <input type="number" id="humidificateurValue" class="input-value form-control" placeholder="Humidité (%)" min="0" max="100" disabled>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activateHumidificateurSchedule" onchange="toggleHumidificateurSchedule(this.checked);">
                            <label class="form-check-label" for="activateHumidificateurSchedule">Activer Horaires</label>
                        </div>
                        <label for="secondHumidificateurValue">Point de consigne secondaire:</label>
                        <input type="number" id="secondHumidificateurValue" class="input-value form-control" placeholder="Humidité (%)" min="0" max="100" disabled>
                        <label for="humidificateurStartTime">Heure de démarrage:</label>
                        <input type="time" id="humidificateurStartTime" class="form-control time-input" disabled>
                        <label for="humidificateurEndTime">Heure de fin:</label>
                        <input type="time" id="humidificateurEndTime" class="form-control time-input" disabled>
                    </div>
                    <!-- Lumière Section -->
                    <div class="section-frame">                         
                        <h2>Lumière<span id="lumiereIcon" class="state-icon">🔴</span></h2>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="activerLight" onchange="toggleLightSection(this.checked);">
                            <label class="form-check-label" for="activerLight">Activer</label>
                            <span class="tooltip">?
                                <span class="tooltiptext">Activer ou désactiver le mode horaire pour l'éclairage avec la plage horaire spécifiée.</span>
                            </span>
                        </div>
                        <label for="lightStartTime">Heure de démarrage Lumière:</label>         
                        <input type="time" id="lightStartTime" class="form-control time-input" disabled>
                        <label for="lightEndTime">Heure de fin Lumière:</label>
                        <input type="time" id="lightEndTime" class="form-control time-input" disabled>                                   
                    </div>
                </div>                                                                                                                                                                   
            </div>                      
            <div class="tab-pane fade show active" id="Dashboard" role="tabpanel" aria-labelledby="dashboard-tab">
                                 
                <div class="row">
                    <div class="col-md-6 mb-4">            
                        <select class="form-control" style="width: 150px;  margin-top: 10px;" onchange="updateGraph(this.value, 'chart1')">
                            <option value="600">Dernière heure</option>
                            <option value="1300">Dernière 3 heures</option>
                            <option value="3600">Dernière 6 heures</option>
                            <option value="16000">Dernier jour</option>
                            <option value="44000">Dernier 3 jours</option>
                            <option value="120800">Dernière semaine</option>
                        </select> 
                        <div class="embed-responsive embed-responsive-16by9">
                            <iframe id="chart1" class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temperature+D1&type=line&xaxis=Time&yaxis=Temperature&yaxismax=40&yaxismin=5" allowfullscreen></iframe>
                        </div>   
                    </div> 
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px ; margin-top: 50px;" src="https://thingspeak.com/channels/1296899/widgets/421466" allowfullscreen></iframe>
                    </div>            
                </div>
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <select class="form-control" style="width: 150px;  margin-top: 10px;" onchange="updateGraph(this.value, 'chart2',2)">
                            <option value="600">Dernière heure</option>
                            <option value="1300">Dernière 3 heures</option>
                            <option value="3600">Dernière 6 heures</option>
                            <option value="16000">Dernier jour</option>
                            <option value="44000">Dernier 3 jours</option>
                            <option value="120800">Dernière semaine</option>
                        </select>          
                        <div class="embed-responsive embed-responsive-16by9">
                            <iframe id="chart2" class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D2&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=50&yaxismin=5"> allowfullscreen></iframe>
                        </div>
                    </div>             
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px; margin-top: 50px;" src="https://thingspeak.com/channels/1296899/widgets/421467" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-4">              
                        <select class="form-control" style="width: 150px;  margin-top: 10px;" onchange="updateGraph(this.value, 'chart3',3)">
                            <option value="600">Dernière heure</option>
                            <option value="1300">Dernière 3 heures</option>
                            <option value="3600">Dernière 6 heures</option>
                            <option value="16000">Dernier jour</option>
                            <option value="44000">Dernier 3 jours</option>
                            <option value="120800">Dernière semaine</option>
                        </select>          
                        <div class="embed-responsive embed-responsive-16by9">
                            <iframe id="chart3" class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D3&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5" allowfullscreen></iframe>
                        </div>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px; margin-top: 50px;" src="https://thingspeak.com/channels/1296899/widgets/421468" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <select class="form-control" style="width: 150px;  margin-top: 10px;" onchange="updateGraph(this.value, 'chart4',4)">
                            <option value="600">Dernière heure</option>
                            <option value="1300">Dernière 3 heures</option>
                            <option value="3600">Dernière 6 heures</option>
                            <option value="16000">Dernier jour</option>
                            <option value="44000">Dernier 3 jours</option>
                            <option value="120800">Dernière semaine</option>
                        </select>            
                        <div class="embed-responsive embed-responsive-16by9">
                            <iframe id="chart4" class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/4?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Temp%C3%A9rature+D4&type=line&xaxis=Time&yaxis=Temp%C3%A9rature&yaxismax=40&yaxismin=5" allowfullscreen></iframe>
                        </div>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px; margin-top: 50px;" src="https://thingspeak.com/channels/1296899/widgets/421469" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <select class="form-control" style="width: 150px;  margin-top: 10px;"  onchange="updateEnvironmentalGraph(this.value, 'chart6', 6)">
                            <option value="600">Dernière heure</option>
                            <option value="1300">Dernière 3 heures</option>
                            <option value="3600">Dernière 6 heures</option>
                            <option value="16000">Dernier jour</option>
                            <option value="44000">Dernier 3 jours</option>
                            <option value="120800">Dernière semaine</option>
                        </select> 
                        <div class="embed-responsive embed-responsive-16by9">
                            <iframe id="chart6" class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/6?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=CO%C2%B2&type=line&xaxis=Time&yaxis=PPM&yaxismax=1000&yaxismin=0" allowfullscreen></iframe>
                        </div>
                    </div>
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px; margin-top: 50px;" src="https://thingspeak.com/channels/1296899/widgets/421472" allowfullscreen></iframe>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-4">
                        <select class="form-control" style="width: 150px;  margin-top: 10px;" onchange="updateEnvironmentalGraph(this.value, 'chart7', 7)">
                            <option value="600">Dernière heure</option>
                            <option value="1300">Dernière 3 heures</option>
                            <option value="3600">Dernière 6 heures</option>
                            <option value="16000">Dernier jour</option>
                            <option value="44000">Dernier 3 jours</option>
                            <option value="120800">Dernière semaine</option>
                        </select>
                        <div class="embed-responsive embed-responsive-16by9">
                            <iframe id="chart7" class="embed-responsive-item w-100" style="height: 300px;" src="https://thingspeak.com/channels/1296899/charts/7?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Humidit%C3%A9&type=line&xaxis=Time&yaxis=%25&yaxismax=100&yaxismin=0" allowfullscreen></iframe>
                        </div>
                    </div>              
                    <div class="col-md-6 embed-responsive embed-responsive-16by9 mb-4">
                        <iframe class="embed-responsive-item w-100" style="height: 300px; margin-top: 50px;" src="https://thingspeak.com/channels/1296899/widgets/421471" allowfullscreen></iframe>
                    </div>
                </div>
            </div>                                                  
        </div>
    </div>
    <script>

        function toggleTimerControl(enabled) {
            document.getElementById('timerOn').disabled = !enabled;
            document.getElementById('timerOff').disabled = !enabled;
            // Disable the other switches when timer is activated
            document.getElementById('activerVent').disabled = enabled;
            document.getElementById('activerHumidity').disabled = enabled;
            if (enabled) {
                document.getElementById('activerVent').checked = false;
                document.getElementById('activerHumidity').checked = false;
                toggleVentilationControl(false);
                toggleHumidityControl(false);
            }
        }
                                                                            
        function toggleTemperatureSection(enabled) {
            document.getElementById('temperatureValue').disabled = !enabled;    
        }

        function toggleHumidificateurSection(enabled) {
            document.getElementById('humidificateurValue').disabled = !enabled;
        }
        function toggleHumidityControl(enabled) {
            document.getElementById('humidityValue').disabled = !enabled;
            // Disable timer switch when this is activated
            document.getElementById('activateTimer').disabled = enabled;
            if (enabled) {
                document.getElementById('activateTimer').checked = false;
                toggleTimerControl(false);
            }
        }                   
                                            
        function toggleHumidificateurSchedule(enabled) {
            document.getElementById('secondHumidificateurValue').disabled = !enabled;
            document.getElementById('humidificateurStartTime').disabled = !enabled;
            document.getElementById('humidificateurEndTime').disabled = !enabled;
            
        }

                                                           

        function setHumidificateur() {
            var humidity = document.getElementById('humidificateurValue').value;
            fetch('/set_humidificateur', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ humidity: humidity }),
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('currentHumidificateur').textContent = humidity;
            })
            .catch(error => console.error('Error:', error));
        }

        function fetchCurrentHumidificateur() {
            fetch('/get_current_humidificateur')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('currentHumidificateur').textContent = data.humidity || 'NA';
                })
                .catch(error => console.error('Error:', error));
        }

        document.getElementById('programming-tab').addEventListener('click', fetchCurrentHumidificateur);

                                                            
        function toggleSecondTemperatureSection(enabled) {
            document.getElementById('secondTemperatureValue').disabled = !enabled;
            document.getElementById('heatingStartTime').disabled = !enabled;
            document.getElementById('heatingEndTime').disabled = !enabled;
        }

        function toggleHumidityInput(enabled) {
            document.getElementById('humidityValue').disabled = !enabled;
            
        }

        function toggleVentilationSection(enabled) {
            document.getElementById('humidityValue2').disabled = !enabled;
            document.getElementById('ventilationStartTime').disabled = !enabled;
            document.getElementById('ventilationEndTime').disabled = !enabled;
        }

        function toggleVentilationControl(enabled) {
           
            document.getElementById('activateTimer').disabled = enabled;
            document.getElementById('humidityValue2').disabled = !enabled;
            document.getElementById('ventilationStartTime').disabled = !enabled;
            document.getElementById('ventilationEndTime').disabled = !enabled;
            if (enabled) {
                document.getElementById('activateTimer').checked = false;
                toggleTimerControl(false);
            }
        }                          

        function toggleLightSection(enabled) {
            document.getElementById('lightStartTime').disabled = !enabled;
            document.getElementById('lightEndTime').disabled = !enabled;
     
        }

        function updateGraph(results, chartId, chartNumber = 1) {
            var src = `https://thingspeak.com/channels/1296899/charts/${chartNumber}?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=${results}&title=Température+D${chartNumber}&type=line&xaxis=Time&yaxis=Température&yaxismax=40&yaxismin=5`;
            document.getElementById(chartId).src = src;
        }
   
        function updateEnvironmentalGraph(results, chartId, chartNumber) {
            let title, yAxisUnit, yAxisMax;
            if (chartNumber === 6) {  // CO2 graph specific parameters
                title = "CO²";
                yAxisUnit = "PPM";
                yAxisMax = 1000;
            } else if (chartNumber === 7) {  // Humidity graph specific parameters
                title = "Humidité";
                yAxisUnit = "%25";  // Encoded "%" for URL
                yAxisMax = 100;
            }

            var src = `https://thingspeak.com/channels/1296899/charts/${chartNumber}?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=${results}&title=${title}&type=line&xaxis=Time&yaxis=${yAxisUnit}&yaxismax=${yAxisMax}&yaxismin=0`;
            document.getElementById(chartId).src = src;
        }                          
                                  
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
                                  
        function setSchedule(device) {
            var start = document.getElementById(device + 'StartTime').value;
            var end = document.getElementById(device + 'EndTime').value;
            fetch('/set_schedule/' + device, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ start: start, end: end }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Schedule set:', data);
            })
            .catch(error => console.error('Error:', error));
        }

        function fetchDeviceStates() {
            updateStateIcon('10.42.0.23', 'chauffageIcon');
            updateStateIcon('10.42.0.130', 'lumiereIcon');
            updateStateIcon('10.42.0.29', 'ventilationIcon');
            updateStateIcon('10.42.0.85', 'humidificateurIcon');
        }
        
        function updateStateIcon(ip, elementId) {
            fetch(`/state/${ip}`)
                .then(response => response.json())
                .then(data => {
                    let icon = '🔴'; 
                    if (data.state === 'ON') {
                        icon = '🟢';
                    } else if (data.state === 'OFF') {
                        icon = '🔴'; 
                    }
                    document.getElementById(elementId).textContent = icon;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById(elementId).textContent = '⚫'; 
                });
        }                                                    

                                  
                                  
        function fetchAverageTemperature() {
            fetch('/get_average_temperature')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('averageTemperature').textContent = data.average_temperature.toFixed(1);
                })
                .catch(error => console.error('Error fetching average temperature:', error));
        }

        function fetchLatestHumidity() {
            fetch('/get_humidity')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('latestHumidity').textContent = data.humidity;
                })
                .catch(error => console.error('Error fetching humidity:', error));
        }

        
        document.addEventListener('DOMContentLoaded', function() {
            fetchAverageTemperature();
            fetchLatestHumidity();
            fetchDeviceStates();
                                  
        });                          

        function clearSchedule(device) {
            fetch('/clear_schedule/' + device, {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                console.log('Schedule cleared:', data);
                document.getElementById(device + 'StartTime').value = '';
                document.getElementById(device + 'EndTime').value = '';
            })
            .catch(error => console.error('Error:', error));
        }

        function fetchSchedule(device) {
            fetch('/get_schedule/' + device)
                .then(response => response.json())
                .then(data => {
                    if (data.start !== 'NA') {
                        document.getElementById(device + 'StartTime').value = data.start;
                    }
                    if (data.end !== 'NA') {
                        document.getElementById(device + 'EndTime').value = data.end;
                    }
                })
                .catch(error => console.error('Error:', error));
        }

        document.getElementById('programming-tab').addEventListener('click', function() {
            fetchDeviceStates(); 
            fetchSchedule('lumiere');
            fetchSchedule('chauffage');
            fetchSchedule('ventilation');
        });                          

        document.getElementById('programming-tab').addEventListener('click', fetchCurrentHumidity);

        function fetchCurrentTemperature() {
            fetch('/get_current_temperature')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('currentTemperature').textContent = data.temperature || 'NA';
                })
                .catch(error => console.error('Erreur:', error));
        }

        
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
        function toggleNightMode() {
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
        function saveSettings() {
            var settings = {
                chauffage: {
                    active: document.getElementById('activerTemp').checked,
                    value: parseFloat(document.getElementById('temperatureValue').value),
                    schedule_active: document.getElementById('activerSecondTemp').checked,
                    schedule: {
                        start: document.getElementById('heatingStartTime').value,
                        end: document.getElementById('heatingEndTime').value
                    },
                    value2: parseFloat(document.getElementById('secondTemperatureValue').value),
                    tempDeadband: parseFloat(document.getElementById('tempDeadband').value)
                },
                ventilation: {
                    active: document.getElementById('activerHumidity').checked,
                    humidity: parseFloat(document.getElementById('humidityValue').value),
                    schedule_active: document.getElementById('activerVent').checked,
                    schedule: {
                        start: document.getElementById('ventilationStartTime').value,
                        end: document.getElementById('ventilationEndTime').value
                    },
                    humidity2: parseFloat(document.getElementById('humidityValue2').value),
                    ventDeadband: parseFloat(document.getElementById('ventDeadband').value),
                    timerOn: parseInt(document.getElementById('timerOn').value),  
                    timerOff: parseInt(document.getElementById('timerOff').value), 
                     timerActive: document.getElementById('activateTimer').checked               
                },
                humidificateur: {
                    active: document.getElementById('activateHumidificateur').checked,
                    humidity: parseFloat(document.getElementById('humidificateurValue').value),
                    schedule_active: document.getElementById('activateHumidificateurSchedule').checked,
                    schedule: {
                        start: document.getElementById('humidificateurStartTime').value,
                        end: document.getElementById('humidificateurEndTime').value
                    },
                    humidity2: parseFloat(document.getElementById('secondHumidificateurValue').value),
                    humDeadband: parseFloat(document.getElementById('humDeadband').value)
                },
                lumiere: {
                    active: document.getElementById('activerLight').checked,
                    schedule: {
                        start: document.getElementById('lightStartTime').value,
                        end: document.getElementById('lightEndTime').value
                    }
                }
            };

            fetch('/save_all_settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(settings)
            })
            .then(response => response.json())
            .then(data => alert('Settings saved successfully!'))
            .catch(error => console.error('Error saving settings:', error));
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
    
        function setTemperature() {
            var temperature = document.getElementById('temperatureValue').value;
            fetch('/set_setting', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({temperature: temperature})
            }).then(response => response.json())
            .then(data => {
                console.log('Temperature updated', data);
            }).catch(error => console.error('Error updating temperature:', error));
        }

        function updateUIWithSettings() {
            fetch('/get_settings')
                .then(response => response.json())
                .then(data => {
                    
                    
                    document.getElementById('activerTemp').checked = data.chauffage.active;
                    document.getElementById('temperatureValue').value = data.chauffage.value || '';
                    document.getElementById('activerSecondTemp').checked = data.chauffage.schedule_active;
                    document.getElementById('secondTemperatureValue').value = data.chauffage.value2 || '';
                    document.getElementById('heatingStartTime').value = data.chauffage.schedule.start || '';
                    document.getElementById('heatingEndTime').value = data.chauffage.schedule.end || '';

                    document.getElementById('ventDeadband').value = data.ventilation.ventDeadband || '';
                    document.getElementById('activerHumidity').checked = data.ventilation.active;
                    document.getElementById('humidityValue').value = data.ventilation.humidity || '';
                    document.getElementById('activerVent').checked = data.ventilation.schedule_active;
                    document.getElementById('humidityValue2').value = data.ventilation.humidity2 || '';
                    document.getElementById('ventilationStartTime').value = data.ventilation.schedule.start || '';
                    document.getElementById('ventilationEndTime').value = data.ventilation.schedule.end || '';
                    document.getElementById('timerOn').value = data.ventilation.timerOn || 0;
                    document.getElementById('timerOff').value = data.ventilation.timerOff || 0;
                    document.getElementById('activateTimer').checked = data.ventilation.timerActive;

                    
                    toggleTimerControl(data.ventilation.timerActive);
                    toggleVentilationControl(data.ventilation.schedule_active);

                    document.getElementById('tempDeadband').value = data.chauffage.tempDeadband || '';
                    document.getElementById('activateHumidificateur').checked = data.humidificateur.active;
                    document.getElementById('humidificateurValue').value = data.humidificateur.humidity || '';
                    document.getElementById('activateHumidificateurSchedule').checked = data.humidificateur.schedule_active;
                    document.getElementById('secondHumidificateurValue').value = data.humidificateur.humidity2 || '';
                    document.getElementById('humidificateurStartTime').value = data.humidificateur.schedule.start || '';
                    document.getElementById('humidificateurEndTime').value = data.humidificateur.schedule.end || '';

                    document.getElementById('humDeadband').value = data.humidificateur.humDeadband || '';
                    document.getElementById('activerLight').checked = data.lumiere.active;
                    document.getElementById('lightStartTime').value = data.lumiere.schedule.start || '';
                    document.getElementById('lightEndTime').value = data.lumiere.schedule.end || '';
                                  
                })
                .catch(error => console.error('Error:', error));
        }


        document.getElementById('programming-tab').addEventListener('click', updateUIWithSettings);
        window.onload = updateUIWithSettings;
                          

        function fetchTemperature() {
            fetch('/get_setting/temperature')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temperatureValue').value = data.temperature || '';
                }).catch(error => console.error('Error fetching temperature:', error));
        }

        document.getElementById('temperatureUpdateButton').addEventListener('click', setTemperature);
        window.onload = fetchTemperature;                          

        function fetchState(ip, elementId) {
            fetch(`/state/${ip}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    let displayState = 'N/A'; // Default state
                    if (data.state && (data.state === 'ON' || data.state === 'OFF')) {
                        displayState = data.state;
                    }
                    document.getElementById(elementId).textContent = displayState;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById(elementId).textContent = 'N/A';
                });
        }
                           
       
        document.getElementById('control-tab').addEventListener('click', updateStates);                             
        
    </script>                                                              
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>                                 
</body>
</html>
""", )



@app.route('/get_settings', methods=['GET'])
def get_settings():
    settings = load_settings()
    return jsonify(settings)

@app.route('/state/<ip>')
def state(ip):
    url = f"http://{ip}/cm?cmnd=Power"
    try:
        response = requests.get(url, timeout=5) 
        response.raise_for_status()  
        state = response.json().get('POWER', 'N/A')
        return jsonify({'state': state})
    except requests.exceptions.HTTPError as e:
        return jsonify({'state': 'N/A', 'error': 'HTTP error'}), 500
    except requests.exceptions.ConnectionError as e:
        return jsonify({'state': 'N/A', 'error': 'Connection error'}), 500
    except Exception as e:
        return jsonify({'state': 'N/A', 'error': str(e)}), 500

    
def load_settings():
    
    try:
        with open(SETTINGS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_settings(settings):
    
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file, indent=4)


@app.route('/update_device_settings', methods=['POST'])
def update_device_settings():
    # This endpoint can be used to update settings for temperature, humidity, or schedules.
    settings_type = request.json.get('type')  # e.g., 'temperature', 'humidity'
    value = request.json.get('value')
    settings = load_settings()
    settings[settings_type] = value
    save_settings(settings)
    return jsonify(status="updated")

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

@app.route('/action/deshumidificateur', methods=['POST'])
def deshumidificateur():
    data = request.get_json()
    ip = data.get('ip')
    url = f"http://{ip}/cm?cmnd=Power%20toggle"
    try:
        response = requests.get(url)
        newState = response.json().get('POWER')
        return jsonify({'state': newState})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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

@app.route('/get_humidity')
def get_humidity():
    response = requests.get("https://api.thingspeak.com/channels/1296899/fields/7.json?api_key=READ_API_KEY")
    if response.ok:
        data = response.json()
        # Assuming the last entry is the most recent
        latest_humidity = data['feeds'][-1]['field7']
        return jsonify({'humidity': latest_humidity})
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

@app.route('/get_average_temperature')
def get_average_temperature():
    fields = [1, 2, 3, 4]
    temperatures = []
    for field in fields:
        response = requests.get(f"https://api.thingspeak.com/channels/1296899/fields/{field}.json?api_key=READ_API_KEY")
        if response.ok:
            data = response.json()
            latest_temperature = data['feeds'][-1][f'field{field}']
            temperatures.append(float(latest_temperature))
        else:
            return jsonify({'error': 'Failed to fetch temperature data'}), 500
    average_temperature = sum(temperatures) / len(temperatures)
    return jsonify({'average_temperature': average_temperature})

@app.route('/set_setting', methods=['POST'])
def set_setting():
    data = request.json
    settings = load_settings()  # Load existing settings
    if 'all' in data['section']:
        settings.update(data['settings'])  # Update all sections if 'all' is specified
    else:
        settings[data['section']].update(data['settings'])  # Update specific section
    save_settings(settings)
    return jsonify(status="success")


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

    data = request.get_json()
    ip = data.get('ip')
    url = f"http://{ip}/cm?cmnd=Power%20toggle"
    try:
        response = requests.get(url)       
        newState = response.json().get('POWER')
        return jsonify({'state': newState})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

   

@app.route('/action/lumiere1', methods=['POST'])
def lumiere1():
    data = request.get_json()
    ip = data.get('ip')
    url = f"http://{ip}/cm?cmnd=Power%20toggle"    
    try:
        response = requests.get(url)       
        newState = response.json().get('POWER')
        return jsonify({'state': newState})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_all_settings', methods=['POST'])
def save_all_settings():
    data = request.get_json()
    settings = load_settings()  # Load existing settings
    settings.update(data)  # Update settings from the request
    save_settings(settings)  # Save updated settings
    return jsonify(status="success")

@app.route('/set_humidificateur', methods=['POST'])
def set_humidificateur():
    data = request.json
    settings = load_settings()
    settings['humidificateur'] = {
        'humidity': data['humidity'],
        'active': data.get('active', False)
    }
    save_settings(settings)
    return jsonify(status="success")

@app.route('/get_current_humidificateur', methods=['GET'])
def get_current_humidificateur():
    settings = load_settings()
    humidity = settings.get('humidificateur', {}).get('humidity', 'NA')
    return jsonify({'humidity': humidity})

   
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
