'''
    @file       publish_ThingSpeak.py
    @date       Avril 2022
    @version    0.1
                Adaptation pour fonctionnalité UDP.
    @brief      Fichier permettant d'envoyer les données vers ThingSpeak.
'''

import paho.mqtt.publish as publish # module pour publié par MQTT
import psutil # proposé avec référence thingspeak
import syst_config  # Fichier des variables, contantes, etc. configurables. 
                    # Permet de modifier les valeurs sans affecter la logique du code.
import getSensors_ds18b20 # valeurs température DS18B20
import getSensors_atlas # valeurs mesures Atlas

#  ThingSpeak Channel Settings
channelID = syst_config.CHANNELID # The ThingSpeak Channel ID 
apiKey = syst_config.APIKEY # The Write API Key for the channel

# Set up the connection parameters based on the connection type
if syst_config.useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None
if syst_config.useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None
if syst_config.useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443       
# Create the topic string
topic = "channels/" + channelID + "/publish" # + apiKey # </debug> Test correction erreur mqtt handshake </>


def push():
    ''' Permet de formatter la payload et de l'envoyer à Thingspeak.
    '''
    global loadDS18B20
    tPayload = getSensors_ds18b20.loadDS18B20 # ajout de la valeur des ds18b20
    
    # ajout des valeurs s'ils sont disponibles
    # si crifa
    if(syst_config.CRIFA) :
        # température capteur humidité
        if getSensors_atlas.tempHVal != -1:
            tPayload += "&field5=" + str(getSensors_atlas.tempVal)
        # co²
        if getSensors_atlas.co2Val != -1:  
            tPayload += "&field6=" + str(getSensors_atlas.co2Val)
        # humidité
        if getSensors_atlas.humVal != -1: 
            tPayload += "&field7=" + str(getSensors_atlas.humVal)
    
    # si hydroponie
    elif(syst_config.HYDROPONIE) :       
        # ph
        if getSensors_atlas.phVal != -1:
            tPayload += "&field3=" + str(getSensors_atlas.phVal)
        # oxygène dissout
        if getSensors_atlas.odVal != -1:
            tPayload += "&field4=" + str(getSensors_atlas.odVal)
        # conductivité
        if getSensors_atlas.ecVal != -1:
            tPayload += "&field5=" + str(getSensors_atlas.ecVal)
        if getSensors_atlas.co2Val != -1:
            tPayload += "&field6=" + str(getSensors_atlas.co2Val)
        
    try:
        #</new publish mqtt>
        print ("Writing Payload = ", tPayload," to host: ", syst_config.MQTTHOST, " to topic: ", topic,
                "\n\tclientID= ", syst_config.MQTT_CLIENTID, "\n\tauth: User=", syst_config.MQTT_USR, " PWD=", syst_config.MQTT_PWD)
        
        publish.single(topic, payload=tPayload, hostname=syst_config.MQTTHOST, transport=tTransport, port=tPort, tls=tTLS,
                        client_id=syst_config.MQTT_CLIENTID, auth={'username':syst_config.MQTT_USR,'password':syst_config.MQTT_PWD})
        #</>
        print ("Published"+"\n")
    except Exception as e:
        print ("There was an error while publishing the data.\nException: ", e)