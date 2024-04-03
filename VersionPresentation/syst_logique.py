'''
    @file       syst_logique.py
    @date       Avril 2022
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Point d'entrée du programme. Ce fichier fichier permet d'exécuter les méthodes
                appartenant aux autres fichiers du répertoire.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
'''
#!/bin/python3

from time import sleep # module pour sleep()
import schedule # module pour événement pushRoutine()
# Fichiers de programmes pour projet Serrebrooke
import syst_config # Fichier des variables, contantes, etc. configurables. Permet de modifier les valeurs sans affecter la logique du code.
import syst_interface # Fichier pour l'affichage physique
import getSensors_ds18b20 # Fichier pour mesures 1-Wire
import getSensors_atlas # Fichier pour mesures Atlas


def main():
    global mainRoot
    
    # Boucle principale
    mainRoot = syst_interface.initAffichage()
    syst_interface.tkiAffiche(pValues=False, pRoot=mainRoot)
    
    while 1:
        # mesure des capteurs 1-Wire et Atlas
        getSensors_ds18b20.getDS18B20() 
        getSensors_atlas.getAtlas()

        syst_interface.tkiAffiche(pRoot=mainRoot) # actualise l'affichage
        sleep(syst_config.tkiDelay) # délai pour l'actualisation de l'affichage. 2sec , donc pause de 2 secondes à la fin du while 
        
# Point d'entrée du programme
if __name__ == '__main__':
    main()
