'''
    @file       getSensors_atlas.py
    @date       Avril 2022
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Ce fichier permet de faire une lecture des capteurs Atlas connecter et d'attribuer cette valeur à une variable.
                Ce fichier utilise la librairie "atlas_i2c".
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
'''

from atlas_i2c import atlas_i2c # module pour capteurs Atlas
import time # module pour sleep
import syst_config # Fichier des variables, contantes, etc. configurables. Permet de modifier les valeurs sans affecter la logique du code.

#création de objets atlas
temp = atlas_i2c.AtlasI2C()
temp.set_i2c_address(syst_config.ADDR_TEMP)

co2 = atlas_i2c.AtlasI2C()
co2.set_i2c_address(syst_config.ADDR_CO2)

hum = atlas_i2c.AtlasI2C()
hum.set_i2c_address(syst_config.ADDR_HUM)


def getAtlas():
    global tempVal, co2Val, tempHVal, humVal # labels qui contiennent les résultats des capteurs.
    global strAtlas # print console

    strAtlas = "" # liste des capteur atlas présent et leurs valeurs 
    
    # init les variables
    tempVal  = 0.0
    co2Val   = 0.0
    tempHVal = 0.0
    humVal   = 0.0
    getMesuresCRIFA()
    print(strAtlas)# print le champ des résultats
    

def getMesuresCRIFA():
    ''' Prends les mesures des capteurs Atlas pour le système en mode CRIFA.
    '''
    global co2, hum # objets des capteurs Atlas
    global tempHVal, co2Val, humVal # labels qui contiennent les résultats des capteurs.
    global strAtlas

    co2Val = getMesure(co2, 'co2=\t', 'co2')
    getMesureHumidite()

def getMesure(obj, strA, sName):
    ''' Effectue une écriture sur le bus I²C pour la lecture du capteur ciblé.
        La valeur obtenue sera de -1 si le capteur est absent.
        @param obj : objet Atlas pour interactions avec I²C
        @param strA : Message affiché à la console
        @param sName : Nom du capteur pour console si exception
        @return Retourne la valeur de la mesure. -1 si le capteur est absent.
    '''
    global strAtlas

    try:
        obj.write("R") # demande une lecture au capteur
        time.sleep(0.9) # délai lecture atlas
        val = round(float((obj.read("R").data).decode("utf-8")),syst_config.PRECISION)  # arrondi et décode la 
                                                                                        # lecture obtenue
        strAtlas += (strA + str(val) + '\n') # ajout de la lecture au champ du terminal

        return val
    
    except Exception as e: # si le capteur est absent
        print("capteur ", sName, " absent") 
        val = -1 # retourne -1
        # print('MessageException:\t', e) # pour debug
    
def getMesureHumidite():
    ''' Permet de récupérer les mesures de température et d'humidité intégrées au capteur 
        d'humidité.
    '''
    global hum, humVal, tempHVal, strAtlas

    try: # capteur humidité-température
        hum.write("R") # demande une lecture au capteur
        time.sleep(0.6) # délai lecture atlas
        HumTempReading = ((hum.read("R").data).decode("utf-8"))
        ListHT_Reading = HumTempReading.split(",")
        humVal = ListHT_Reading[0]
        tempHVal = ListHT_Reading[1]
        strAtlas += ('hum=\t' + str(humVal) + '\n') # ajout de la lecture à la string du topic MQTT
        strAtlas += ('tempH=\t' + str(tempHVal) + '\n') # ajout de la lecture à la string du topic MQTT
    
    except Exception as e:
        print("capteur humidité absent") # si le capteur n'est pas détecté
        humVal = -1 # si le capteur est absent, retourne -1
        tempHVal = -1
        # print('MessageException:\t', e) # pour debug
