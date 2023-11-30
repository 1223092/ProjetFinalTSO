'''
    @file       publish_UDP.py
    @author     equipe-projet-peridoseur
    @date       Avril 2022
    @version    0.2
                Adaptation pour capteurs DS18B20 multiples.
    @brief      Fichier permettant d'envoyer les données des capteurs par UDP.
'''


import syst_config #Fichier des variables, contantes, etc. configurables. Permet de modifier les valeurs sans affecter la logique du code.
import getSensors_ds18b20
import getSensors_atlas
import socket
import ipaddress
import json
import os
import requests


ENCODING = "utf-8"


# Set up the connection parameters based on the connection type
if syst_config.useUnsecuredUDP:
    # format pour extraire les valeurs d'environnement pour l'adresse ip.
    balenaAddr = os.getenv('BALENA_SUPERVISOR_ADDRESS')
    balenaAPI = os.getenv('BALENA_SUPERVISOR_API_KEY')
    balenaContent = requests.get(balenaAddr+"/v1/device?apikey="+balenaAPI, headers={"content-type":"application/json"}).content
    # configuration pour communication udp
    Port1 = 4444
    Port2 = 5858
    Mask = '255.255.255.0'
    ipaddr = (json.loads(balenaContent.decode(ENCODING)))["ip_address"] # decode la ligne en json et extrait la valeur de l'adresse ip
    network = ipaddress.IPv4Network(ipaddr+'/'+Mask, False)
    Broadcast = str(network.broadcast_address)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # pour permettre l'envoi par UDP

#Sépare les données float en partie entière et décimale, puis ajoute les à une list
def floatSplitter(array,value):
    entier = int(value)
    decimal = int((value - entier)*10)
    array.append(entier)
    array.append(decimal)

#formation de la Payload et envois de la valeur des capteurs a thingspeak
def push():
    global loadDS18B20, brd, Port
    jPayload = {} # pour les données en format JSON
    tPayload = {} # pour rassembler les données
    #tPayload.append(1)

    iTempVal = 1 # index pour le json des ds18b20
    for tVal in getSensors_ds18b20.tempUDP:
        tPayload[f"t{iTempVal}"] = tVal #ajout de la valeur des ds18b20
        jPayload[f"temp{iTempVal}"] = tVal
        iTempVal+=1
    
    if(syst_config.CRIFA) :
        if getSensors_atlas.tempVal != -1:#ajout de la valeur du capteur si il est present
            tPayload["t"] = getSensors_atlas.tempVal       
            jPayload["temp"] = getSensors_atlas.tempVal
        if getSensors_atlas.co2Val != -1:#ajout de la valeur du capteur si il est present
            tPayload["c"] = getSensors_atlas.co2Val
            jPayload["co2"] = getSensors_atlas.co2Val
        if getSensors_atlas.humVal != -1:#ajout de la valeur du capteur si il est present
            tPayload["h"] = getSensors_atlas.humVal
            jPayload["hum"] = getSensors_atlas.humVal
    if(syst_config.HYDROPONIE) :       
        if getSensors_atlas.tempVal != -1:#ajout de la valeur du capteur si il est present
            tPayload[f"t{iTempVal}"] = getSensors_atlas.tempVal
            jPayload["tempAtlas"] = getSensors_atlas.tempVal       
        if getSensors_atlas.phVal != -1:#ajout de la valeur du capteur si il est present
            tPayload["p"] = getSensors_atlas.phVal
            jPayload["pH"] = getSensors_atlas.phVal       
        if getSensors_atlas.ecVal != -1:#ajout de la valeur du capteur si il est present
            tPayload["e"] = getSensors_atlas.ecVal
            jPayload["ec"] = getSensors_atlas.ecVal
        if getSensors_atlas.odVal != -1:#ajout de la valeur du capteur si il est present
            tPayload["o"] = getSensors_atlas.odVal
            jPayload["od"] = getSensors_atlas.odVal
        if getSensors_atlas.orpVal != -1:#ajout de la valeur du capteur si il est present
            tPayload["or"] = getSensors_atlas.orpVal
            jPayload["orp"] = getSensors_atlas.orpVal
    
    #calcul et ajout du checksum
    #chk = 0
    #for x in range(len(tPayload)-1):
    #    chk += tPayload[x+1]
    #chk = chk & 0xFF
    #tPayload.append(chk)
    
    try:
        #sock.sendto(bytearray(tPayload), (Broadcast, Port))
        sock.sendto(bytes(json.dumps(tPayload), ENCODING), (Broadcast, Port1))
        sock.sendto(bytes(json.dumps(jPayload), ENCODING), (Broadcast, Port2))
        print ("Published on UDP"+"\n")
        #time.sleep(10)
    except:
        print ("There was an error while publishing the data.")
        
        
