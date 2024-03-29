# Répertoire du programme du serveur d'acquisitions

## Description des fichiers
### Notes
#### Dernière révision des fichiers
    @date   2023-12-22
###### syst_config.py
    @file       syst_config.py
    @date       Avril 2024
    @version    0.2
                
    @brief      Fichier des variables, contantes, etc. configurables.
                Permet de modifier les valeurs sans affecter la logique du code.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
###### syst_logique.py
    @file       syst_logique.py
    @date       Avril 2024
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Point d'entrée du programme. Ce fichier fichier permet d'exécuter les méthodes
                appartenant aux autres fichiers du répertoire.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
###### syst_interface.py
    @file       syst_interface.py
    @date       Janvier 2024
    @version    0.0 : Première version
    @brief      Fichier du programme pour l'interface physique. Permet de définir
                les fonctions pour sa construction.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
###### getSensors_atlas.py
    @file       getSensors_ds18b20.py
    @date       Avril 2024
    @version    0.2
                Ajout d'une autre condition s'il y a trop de capteurs ou aucun.
                Adaptation pour fonctionnalité UDP.
    @brief      Ce fichier permet de faire une lecture des capteurs ds18b20 connecter et d'attribuer cette valeur à une variable.
                Ce fichier utilise la librairie "W1ThermSensor".
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
###### publish_ThingSpeak.py
    @file       publish_ThingSpeak.py
    @date       Avril 2024
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Fichier permettant d'envoyer les données vers ThingSpeak.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
###### publish_UDP.py
    @file       publish_UDP.py
    @author     equipe-projet-peridoseur
    @date       Avril 2024
    @version    0.1
                Adaptation pour capteurs DS18B20 multiples.
    @brief      Fichier permettant d'envoyer les données des capteurs par UDP.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
##### tab.py
    @file       tab.py
    @date       Avril 2024
    @version    0.1
                Interface web.
    @brief      Ce fichier comprend le page web
                Il récupère les valeurs critiques pour la gestion des boucles de contrôle.
                Gestion de la communication avec les prises intelligentes via le point d'accès WIFI.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
