# Répertoire du programme du serveur d'acquisitions

## Description des fichiers
### Notes
#### Dernière révision des fichiers
    @date   2023-12-22
###### syst_config.py
    @file       syst_config.py
    @date       Avril 2022
    @version    0.2
                Adaptation pour code NFT
    @brief      Fichier des variables, contantes, etc. configurables.
                Permet de modifier les valeurs sans affecter la logique du code.
###### syst_logique.py
    @file       syst_logique.py
    @date       Avril 2022
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Point d'entrée du programme. Ce fichier fichier permet d'exécuter les méthodes
                appartenant aux autres fichiers du répertoire.
###### syst_interface.py
    @file       syst_interface.py
    @date       Janvier 2022
    @version    0.0 : Première version
    @brief      Fichier du programme pour l'interface physique. Permet de définir
                les fonctions pour sa construction.
###### getSensors_atlas.py
    @file       getSensors_ds18b20.py
    @date       Avril 2022
    @version    0.2
                Ajout d'une autre condition s'il y a trop de capteurs ou aucun.
                Adaptation pour fonctionnalité UDP.
    @brief      Ce fichier permet de faire une lecture des capteurs ds18b20 connecter et d'attribuer cette valeur à une variable.
                Ce fichier utilise la librairie "W1ThermSensor".
###### publish_ThingSpeak.py
    @file       publish_ThingSpeak.py
    @date       Avril 2022
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Fichier permettant d'envoyer les données vers ThingSpeak.
###### publish_UDP.py
    @file       publish_UDP.py
    @author     equipe-projet-peridoseur
    @date       Avril 2022
    @version    0.1
                Adaptation pour capteurs DS18B20 multiples.
    @brief      Fichier permettant d'envoyer les données des capteurs par UDP.
##### Controle_GPIO.py
    @file       Controle_GPIO.py
    @date       decembre 2023
    @version    9.0 : 
    @brief      script Python utilise Flask pour créer une application web permettant de contrôler et de suivre l'état des ports GPIO d'un Raspberry Pi.