'''
    @file       syst_config.py
    @date       Avril 2022
    @version    0.2
                Adaptation pour code NFT
    @brief      Fichier des variables, contantes, etc. configurables.
                Permet de modifier les valeurs sans affecter la logique du code.
'''

#Configuration du sytème. L'affichage et les capteurs utilisés changent en fonction de la configuration choisie.
HYDROPONIE = False
CRIFA = True

## Publish Thingspeak
# Pour les valeurs d'identification des différents channels, voir la fin du fichier.
#  MQTT Connection Methods
useUnsecuredTCP = False             # Set useUnsecuredTCP to True to use the default MQTT port of 1883
useUnsecuredWebsockets = True       # Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
                                    # Try this if port 1883 is blocked on your network.
useSSLWebsockets = False            # Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
MQTTHOST = "mqtt3.thingspeak.com"    # The Hostname of the ThinSpeak MQTT service

## Publish PLC
# UDP Connection
useUnsecuredUDP = False

# Fréquence d'acquisition
tkiDelay = 2 # délai par défaut de l'aquisition des mesures
tsDelay = 10 # delai d'intervalle au minutes pour envoyer les donnees sur thingspeak

# Mesures
PRECISION = 1 # précision décimale, nombres de décimales
PHTEMP = True # mode compensation du ph avec la température pour plus de pression

# Atlas
# adresse d'origine des capteurs (disponible sur la documentation atlas)
ADDR_PH = 0x63     
ADDR_TEMP = 0x66    
ADDR_EC = 0x64      
ADDR_OD = 0x61     
ADDR_CO2 = 0x69    
ADDR_HUM = 0x6F    
ADDR_ORP = 0x62

# Interface
TKI_FULLSCREEN = True       # mode plein écran
TKI_RESOLUTION = "1024x600" # résolution de l'écran
TKI_NULLMESSAGE = "--"      # string à afficher si valeur nulle
TKI_BACKCOLOR = "black"     # couleur de fond
TKI_TEXTCOLOR = "white"     # couleur de texte
TKI_FONT = "courier"       # style de police du texte

# position de la fenêtre 
TKPOS_LEFT = 0.02
TKPOS_CENTER = 0.35
TKPOS_RIGHT = 0.68
TKPOS_TOP = 0.05
TKPOS_MIDDLE = 0.33
TKPOS_BOTTOM = 0.70
TKPOS_OFFSET = 0.04

# dimension
TKLEN_BTN = 20 # longeur des boutons
TKLEN_LBL = 20 # taille du texte
TKLEN_VAR = 30 # taille du texte des variables



### </END OF FILE>
## Valeurs du channel ThingSpeak

# SERREBROOKE-NFT
if HYDROPONIE:
    CHANNELID = "1328019"       # Channel Serrebrooke-NFT
    APIKEY = "VMDDBI3TNI7BRQQE" # API Key

    MQTT_CLIENTID = "EgMZGAssAScsHSopOxs1AhM"
    MQTT_USR = "EgMZGAssAScsHSopOxs1AhM"
    MQTT_PWD = "1M9oQc1vtIU3IFjGKwtxdXns"

# CRIFA
elif CRIFA:
    CHANNELID = "1296899"       # Channel CRIFA
    APIKEY = "H760997692T443A5" # API Key

    MQTT_CLIENTID = "JhwfFC0RLSsgHhI4MTkKLwo"
    MQTT_USR = "JhwfFC0RLSsgHhI4MTkKLwo"
    MQTT_PWD = "an8oTonCcaxFMvLBHmhnA1E6"

# PERIDOSEUR-TEST
# CHANNELID = "1676290"       # Channel
# APIKEY = "OKPWRAN4HVISPK1V" # API Key