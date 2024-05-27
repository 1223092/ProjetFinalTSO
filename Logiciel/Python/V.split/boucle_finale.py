'''
    @file       boucle_finale.py
    @date       Mai 2024
    @version    0.1
                
    @brief      Fichier du programme contenant les boucles controlant l'activation des systèmes de contrôle environnementales
                de la serre selon les commandes demandés depuis le site web.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python      
'''
#Librairies Python
import requests
import time
from datetime import datetime
import json
import threading

# Fichiers du programme Serrebrooke
import getSensors_ds18b20
import getSensors_atlas

# URLs des prises Tasmota
HEATER_URL = "http://10.42.0.23/cm?cmnd=Power%20"
VENTILATION_URL = "http://10.42.0.88/cm?cmnd=Power%20"
LUMIERE_URL = "http://10.42.0.130/cm?cmnd=Power%20"
HUMIDIFICATEUR_URL = "http://10.42.0.85/cm?cmnd=Power%20"

# Fichier pour stocker les paramètres
SETTINGS_FILE = '/root/app-serrebrooke/control_settings.json'


# Methode qui récupère les paramètres principales..................................
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return initialize_default_settings()

# Methode qui initialise et retourne les paramètres par défault si le fichier de confiugrations est introuvable.    
def initialize_default_settings():
    """ Initialize and return default settings if file is not found. """
    default_settings = {
        "chauffage": {"active": False, "value": None, "schedule_active": False, "schedule": {}, "value2": None},
        "ventilation": {"active": False, "humidity": None, "schedule_active": False, "schedule": {}, "humidity2": None, "timerOn": None, "timerOff": None, "timerActive": False},
        "humidificateur": {"active": False, "humidity": None, "schedule_active": False, "schedule": {}, "humidity2": None},
        "lumiere": {"active": False, "schedule": {}}
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(default_settings, f, indent=4)
    return default_settings    


# Methode qui envoie la commande à la prise intelligente.
def control_device(url, command):
    try:
        response = requests.get(url + command)
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur de connexion: {e}")

# Méthode qui vérifie si l'heure actuelle est dans l'intervalle spécifié.
def check_time_in_range(start, end, current):
    current_time = current.time()
    return start <= current_time <= end

# Méthode qui permet de sélectionner des durées de temps pour le contrôle intermittent de la ventilation.
def timer_control(url, timer_on, timer_off, active_check):
    
    while True:
        if not active_check():
            break  
        control_device(url, "on")
        time.sleep(timer_on)
        if not active_check():
            break
        control_device(url, "off")
        time.sleep(timer_off * 60) 

# Méthode principale qui récupère les données de contrôle et qui les appliquent aux systèmes
# selon les paramètres demandés.
def main_loop():
    timer_threads = {}

    while True:
        settings = load_settings()
        current_time = datetime.now()

        # Obtention des valeurs actuelles des capteurs
        temp = getSensors_ds18b20.getDS18B20()
        tempmoy = temp[-1]  # Température moyenne
        
        getSensors_atlas.getAtlas()
        humVal = float(getSensors_atlas.humVal)

        # Deadband : valeur de chevauchement par rapport aux valeurs demandés.
        temp_deadband = settings.get('chauffage', {}).get('tempDeadband', 2)  
        vent_deadband = settings.get('ventilation', {}).get('ventDeadband', 5)   
        hum_Deadband = settings.get('humidificateur', {}).get('humDeadband', 5)

        # Gestion du chauffage
        if settings['chauffage']['schedule_active']:
            start = datetime.strptime(settings['chauffage']['schedule']['start'], '%H:%M').time()
            end = datetime.strptime(settings['chauffage']['schedule']['end'], '%H:%M').time()
            if check_time_in_range(start, end, current_time):
                desired_temp = settings['chauffage']['value2']
            else:
                desired_temp = settings['chauffage']['value']
        elif settings['chauffage']['active']:
            desired_temp = settings['chauffage']['value']
        else:
            desired_temp = None

        if desired_temp is not None:
            if tempmoy > desired_temp + temp_deadband:
                control_device(HEATER_URL, "off")
            elif tempmoy < desired_temp - temp_deadband:
                control_device(HEATER_URL, "on")

        # Gestion de la ventilation
        if settings['ventilation']['schedule_active']:
            start = datetime.strptime(settings['ventilation']['schedule']['start'], '%H:%M').time()
            end = datetime.strptime(settings['ventilation']['schedule']['end'], '%H:%M').time()
            if check_time_in_range(start, end, current_time):
                desired_humidity = settings['ventilation']['humidity2']
            else:
                desired_humidity = settings['ventilation']['humidity']
        elif settings['ventilation']['active']:
            desired_humidity = settings['ventilation']['humidity']
        else:
            desired_humidity = None
        
        if desired_humidity is not None:
            if humVal > desired_humidity + vent_deadband:
                control_device(VENTILATION_URL, "on")
            elif humVal < desired_humidity - vent_deadband:
                control_device(VENTILATION_URL, "off")


        if settings['ventilation']['timerActive']:
            if 'ventilation' not in timer_threads or not timer_threads['ventilation'].is_alive():
               
                timer_threads['ventilation'] = threading.Thread(target=timer_control,
                                                                args=(VENTILATION_URL, settings['ventilation']['timerOn'], settings['ventilation']['timerOff'],
                                                                      lambda: settings['ventilation']['timerActive']))
                timer_threads['ventilation'].start()
        else:
            if 'ventilation' in timer_threads and timer_threads['ventilation'].is_alive():
                
                timer_threads['ventilation'].join()
                          
        # Gestion de l'humidité
        if settings['humidificateur']['schedule_active']:
            start = datetime.strptime(settings['humidificateur']['schedule']['start'], '%H:%M').time()
            end = datetime.strptime(settings['humidificateur']['schedule']['end'], '%H:%M').time()
            if check_time_in_range(start, end, current_time):
                desired_humidity = settings['humidificateur']['humidity2']
            else:
                desired_humidity = settings['humidificateur']['humidity']
        elif settings['humidificateur']['active']:
            desired_humidity = settings['humidificateur']['humidity']
        else:
            desired_humidity = None

        if desired_humidity is not None:
            if humVal > desired_humidity + hum_Deadband:
                control_device(HUMIDIFICATEUR_URL, "off")
            elif humVal < desired_humidity - hum_Deadband:
                control_device(HUMIDIFICATEUR_URL, "on")

        # Gestion de la lumière
        if settings['lumiere']['active']:
            start = datetime.strptime(settings['lumiere']['schedule']['start'], '%H:%M').time()
            end = datetime.strptime(settings['lumiere']['schedule']['end'], '%H:%M').time()
            if check_time_in_range(start, end, current_time):
                control_device(LUMIERE_URL, "on")
            else:
                control_device(LUMIERE_URL, "off")

        time.sleep(5)  

if __name__ == '__main__':
    main_loop()
