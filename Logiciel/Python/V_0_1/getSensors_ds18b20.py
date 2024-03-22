'''
    @file       getSensors_ds18b20.py
    @date       Avril 2022
    @version    0.2
                Ajout d'une autre condition s'il y a trop de capteurs ou aucun.
                Adaptation pour fonctionnalité UDP.
    @brief      Ce fichier permet de faire une lecture des capteurs ds18b20 connecter et d'attribuer cette valeur à une variable.
                Ce fichier utilise la librairie "W1ThermSensor".
'''

from w1thermsensor import W1ThermSensor # module 1-wire
import syst_config # Fichier des variables, contantes, etc. configurables. Permet de modifier les valeurs sans affecter la logique du code.

def getDS18B20():
    ''' Permet de faire la lecture des capteurs 1-Wire. Récupère le nombre de DS18B20 disponible
        et effectue la lecture dans l'ordre de la vitesse de leurs réponses.

        Note:   À chaque reboot du système, les capteurs ont la possibilité de swap 
                leurs positions.
    '''
    global loadDS18B20, strDS18B20 # pour payload Thingspeak
    global temp1, temp2, temp3, temp4, tempUDP, tempMOY # labels températures
    
    nombreDS18B20 = 0 #pour la numerotation (temp1, temp2 ...)
    strDS18B20 = '' #texte de la valeur des capteurs
    loadDS18B20 = ''

    try:
        nbSensors = W1ThermSensor.get_available_sensors() # doit donner la liste des ds18b20 disponibles.
        nbSensors = sorted(nbSensors, key=lambda x: x.id) # ca devrait mettre les capteurs en ordre croissant d'ID.
        tempUDP = [0]*len(nbSensors) # ajout d'une liste pour les ds18b20 disponibles

        for sensor in nbSensors:  # pour chaque sensor ds18b20 disponible
            W1ThermSensor.exists # capteur disponible?
            # nouvelle valeur
            nombreDS18B20 += 1 # incrémentation du nombre de capteurs
            temp = round(sensor.get_temperature(), syst_config.PRECISION) # recupère la valeur du capteur
         
            strDS18B20+=('temperature'+str(nombreDS18B20)+' = '+str(temp)+'\n') # ajout de la données à la payload
                                                                                # pour Thingspeak.
            
            # attribution aux champs textes
            # formattage du field à envoyer
            if nombreDS18B20 == 1:
                temp1 = temp
                loadDS18B20 += "&field" + str(nombreDS18B20) + "=" + str(temp1)
                tempUDP[nombreDS18B20-1] = temp # champ pour udp

            elif nombreDS18B20 == 2:
                temp2 = temp
                loadDS18B20 += "&field" + str(nombreDS18B20) + "=" + str(temp2)
                tempUDP[nombreDS18B20-1] = temp
            
            elif nombreDS18B20 == 3:
                temp3 = temp
                loadDS18B20 += "&field" + str(nombreDS18B20) + "=" + str(temp3)
                tempUDP[nombreDS18B20-1] = temp

            elif nombreDS18B20 == 4:
                temp4 = temp
                loadDS18B20 += "&field" + str(nombreDS18B20) + "=" + str(temp4)
                tempUDP[nombreDS18B20-1] = temp
            
            # si plus de capteurs que supposés?
            elif nombreDS18B20 > 4:
                print("erreur: Trop de DS18B20 connectés")
            # si aucun capteur?
            else:
                print("erreur: aucun connecteurs connectés")
            
        tempMOY = round((temp1+temp2+temp3+temp4)/4 , syst_config.PRECISION)
    except:
        print("erreur strD")
        
    return temp1, temp2, temp3, temp4, tempUDP, tempMOY
    nombreDS18B20 = 0 #remise a zero de le numerotation des capteur
    
