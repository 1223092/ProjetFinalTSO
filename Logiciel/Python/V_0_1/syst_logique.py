'''
    @file       syst_logique.py
    @date       Avril 2022
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Point d'entrée du programme. Ce fichier fichier permet d'exécuter les méthodes
                appartenant aux autres fichiers du répertoire.
'''
#!/bin/python3

from time import sleep # module pour sleep()
import schedule # module pour événement pushRoutine()
# Fichiers de programmes pour projet Serrebrooke
import syst_config # Fichier des variables, contantes, etc. configurables. Permet de modifier les valeurs sans affecter la logique du code.
import syst_interface # Fichier pour l'affichage physique
import getSensors_ds18b20 # Fichier pour mesures 1-Wire
import getSensors_atlas # Fichier pour mesures Atlas
import publish_ThingSpeak # Fichier pour publié les données sur Thingspeak
import publish_UDP # Fichier pour publié les données par UDP (Complémentaire avec projet Péridoseur)
import socket


def pushRoutine():
    ''' Routine qui execute le code a l'intervalle determinee.
    '''
    # si un des types de connexions MQTT est vrai?
    if syst_config.useSSLWebsockets|syst_config.useUnsecuredTCP|syst_config.useUnsecuredWebsockets:
        publish_ThingSpeak.push() # publie sur thingspeak
    # si connexion UDP vrai?
    if syst_config.useUnsecuredUDP:
        publish_UDP.push()



def main():
    global mainRoot
    
    # Boucle principale
    mainRoot = syst_interface.initAffichage()
    syst_interface.tkiAffiche(pValues=False, pRoot=mainRoot)
    
    #Creation d'une routine qui sera publié à toutes le X secondes
    schedule.every(syst_config.tsDelay).seconds.do(pushRoutine)
    
    cptDelay = 0    # compteur pour les 10 premiers envois sur Thingspeak. Applicable principalement
                    # au système CRIFA, puisque le délai est long. (habituellement 30 min)
    while 1:
        # mesure des capteurs 1-Wire et Atlas
        getSensors_ds18b20.getDS18B20() 
        getSensors_atlas.getAtlas()

        # Pour les 10 premieres acquisitions...
        # else, on utilise l'événement pushRoutine()
        if cptDelay < 10:
            pushRoutine() # publie les données
            cptDelay+=1
        else:
            # Appel la routine de schedule
            schedule.run_pending() # routine schedule

        syst_interface.tkiAffiche(pRoot=mainRoot) # actualise l'affichage
        sleep(syst_config.tkiDelay) # délai pour l'actualisation de l'affichage. 2sec , donc pause de 2 secondes à la fin du while 
        
# Point d'entrée du programme
if __name__ == '__main__':
    main()