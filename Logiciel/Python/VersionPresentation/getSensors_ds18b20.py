'''
    @file       getSensors_ds18b20.py
    @date       Avril 2024
    @version    0.2
                Ajout d'une autre condition s'il y a trop de capteurs ou aucun.
                Adaptation pour fonctionnalité UDP.
    @brief      Ce fichier permet de faire une lecture des capteurs ds18b20 connecter et d'attribuer cette valeur à une variable.
                Ce fichier utilise la librairie "W1ThermSensor".
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
'''

from w1thermsensor import W1ThermSensor # module 1-wire
import syst_config # Fichier des variables, contantes, etc. configurables. Permet de modifier les valeurs sans affecter la logique du code.

def getDS18B20():
    ''' Permet de faire la lecture des capteurs 1-Wire. Récupère le nombre de DS18B20 disponible
        et effectue la lecture dans l'ordre de la vitesse de leurs réponses.

        Note:   À chaque reboot du système, les capteurs ont la possibilité de swap 
                leurs positions.
    '''
    global temp # labels températures

    try:
        nbSensors = W1ThermSensor.get_available_sensors() # doit donner la liste des ds18b20 disponibles.
        nbSensors = sorted(nbSensors, key=lambda x: x.id) # ca devrait mettre les capteurs en ordre croissant d'ID.
        tempUDP = [0]*len(nbSensors) # ajout d'une liste pour les ds18b20 disponibles

        for sensor in nbSensors:  # pour chaque sensor ds18b20 disponible
            W1ThermSensor.exists # capteur disponible?
            # nouvelle valeur
            
            temp = round(sensor.get_temperature(), syst_config.PRECISION) # recupère la valeur du capteur
         
            
    except:
        print("erreur strD")
        
    
