#Loic Sarhy
#Boucle qui part les systèmes de controle d'environnement
#

import RPi.GPIO as GPIO  # Importe la bibliothèque pour contrôler les GPIO sur Raspberry Pi
import getSensors_atlas as atlas
import getSensors_ds18b20 as temp


setpointHigh = 30
setpointLow = 0

# Configuration initiale des ports GPIO
GPIO.setmode(GPIO.BCM)  # Utilisation de la numérotation BCM pour les ports GPIO
GPIO.setwarnings(False)  # Désactivation des avertissements GPIO
ports = [16, 19 ,26]  # Liste des ports GPIO utilisés
for port in ports:
    GPIO.setup(port, GPIO.OUT)  # Configure chaque port en mode sortie




def verif():
    if(temp.temp1 < setpointLow ):
        GPIO.output(16, GPIO.HIGH)
    elif(temp.temp1 > setpointHigh):
        GPIO.output(16, GPIO.LOW)
    else:
        GPIO.output(16, GPIO.LOW)

