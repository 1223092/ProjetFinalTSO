'''
    @file       syst_logique.py
    @date       Avril 2024
    @version    0.1
                
    @brief      Point d'entrée du programme. Ce fichier fichier permet d'exécuter les méthodes
                appartenant aux autres fichiers du répertoire. C'est à partir de ce fichier que la demade de prises de mesures 
                et l'envoye de données sont effectués.
                données sont

    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
'''
#!/bin/python3

#Librairies Python
import time
from datetime import datetime # module pour le temps
import schedule # module pour événement pushRoutine()
import socket
import threading

# Fichiers du programme Serrebrooke
import syst_config # Fichier des variables, contantes, etc. configurables. Permet de modifier les valeurs sans affecter la logique du code.
import syst_interface # Fichier pour l'affichage physique
import getSensors_ds18b20 # Fichier pour mesures 1-Wire
import getSensors_atlas # Fichier pour mesures Atlas
import publish_ThingSpeak # Fichier pour publié les données sur Thingspeak
import publish_UDP # Fichier pour publié les données par UDP (Complémentaire avec projet Péridoseur)
from boucle_finale import main_loop


global internet

def pushRoutine():
    ''' Routine qui execute le code a l'intervalle determinee.
    '''
    try :
        # si un des types de connexions MQTT est vrai?
        if syst_config.useSSLWebsockets|syst_config.useUnsecuredTCP|syst_config.useUnsecuredWebsockets:
            publish_ThingSpeak.push() # publie sur thingspeak
            internet = "ON"
        # si connexion UDP vrai?
        if syst_config.useUnsecuredUDP:
            publish_UDP.push()
            internet = "ON"
    except socket.error as e :
        print("An error occurred:", e)
        internet = "OFF"
        # Handle the error gracefully, possibly log it
        # Here, you can continue executing the rest of your code

def getTime():
    
    return time.strftime("%H:%M", time.localtime())


def main():

    ''' Fonction principale du programme, initialise l'affichage et gère la logique d'acquisition des données. '''
    mainRoot = syst_interface.initAffichage()
    syst_interface.tkiAffiche(pValues=False, pRoot=mainRoot)

    # Définit la fréquence de publication des données.
    schedule.every(syst_config.tsDelay).seconds.do(pushRoutine)
    cptDelay = 0  # Compteur pour le début rapide des envois
    thread = threading.Thread(target=main_loop)
    thread.start()
    while True:
        # Acquisition des données des capteurs
        getSensors_ds18b20.getDS18B20()
        getSensors_atlas.getAtlas()

        if cptDelay < 10:
            pushRoutine()
            cptDelay += 1
        else:
            schedule.run_pending()

        # Mise à jour de l'affichage
        syst_interface.tkiAffiche(pRoot=mainRoot)
        time.sleep(syst_config.tkiDelay)  # Délai d'actualisation de l'interface

if __name__ == '__main__':
    main()