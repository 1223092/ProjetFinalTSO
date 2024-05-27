'''
    @file       site_final.py
    @date       Avril 2024
    @version    0.1
                
    @brief      Fichier qui gère les requêtes web. Envoie des commandes aux
                prises intelligentes pour les activer/desactiver, donc démarrer/éteindre
                les systèmes HVAC.

    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
'''

#Librairies Python
from flask import Flask, render_template, jsonify, request, Response ,redirect
import requests
import json 

app = Flask(__name__)
#SETTINGS_FILE = 'control_settings.json'
SETTINGS_FILE = '/root/app-serrebrooke/control_settings.json'
CHANNEL_ID = "1328019"
READ_API_KEY = "NE9WSA72L91KCA9W"

# Adresses IP des prises intelligentes
DEVICE_IPS = {
    "HEATER": "10.42.0.29",
    "VENTILATION": "10.42.0.88",
    "LUMIERE": "10.42.0.130",
    "HUMIDIFICATEUR": "10.42.0.85"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
  

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

#########################################
#      Téléchargement des données       #
#########################################
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




#####################################
#     Récuperation des données      #
#####################################

@app.route('/get_humidity')
def get_humidity():
    response = requests.get("https://api.thingspeak.com/channels/1328019/fields/7.json?api_key=READ_API_KEY")
    if response.ok:
        data = response.json()
        # Assuming the last entry is the most recent
        latest_humidity = data['feeds'][-1]['field7']
        return jsonify({'humidity': latest_humidity})
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500
    

@app.route('/get_current_humidificateur', methods=['GET'])
def get_current_humidificateur():
    settings = load_settings()
    humidity = settings.get('humidificateur', {}).get('humidity', 'NA')
    return jsonify({'humidity': humidity})


@app.route('/get_average_temperature')
def get_average_temperature():
    fields = [1, 2, 3, 4]
    temperatures = []
    for field in fields:
        response = requests.get(f"https://api.thingspeak.com/channels/1328019/fields/{field}.json?api_key=READ_API_KEY")
        if response.ok:
            data = response.json()
            latest_temperature = data['feeds'][-1][f'field{field}']
            temperatures.append(float(latest_temperature))
        else:
            return jsonify({'error': 'Failed to fetch temperature data'}), 500
    average_temperature = sum(temperatures) / len(temperatures)
    return jsonify({'average_temperature': average_temperature})



#########################################
#             Paramètres               #
########################################
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


@app.route('/save_all_settings', methods=['POST'])
def save_all_settings():
    data = request.get_json()
    settings = load_settings()  # Load existing settings
    settings.update(data)  # Update settings from the request
    save_settings(settings)  # Save updated settings
    return jsonify(status="success")


###############################################
#       Controle des systèmes HVAC           #
##############################################
# Section des methodes qui active ou désactive les prises intelligentes

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



###########################
#         Main            #
###########################   
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
