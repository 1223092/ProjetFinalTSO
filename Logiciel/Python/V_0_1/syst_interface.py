'''
    @file       syst_interface.py
    @date       Mars 2022
    @version    0.1
                Ajout de try/catch pour gérer les exceptions faites lors de la
                récupération des données des capteurs lorsqu'ils sont absents.
                
    @brief      Fichier du programme pour l'interface physique. Permet de définir
                les fonctions pour sa construction et de récupérer les valeurs des
                lectures de capteurs pour actualiser l'affichage.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
'''
from time import sleep # pour fonction sleep()
import tkinter as tk # module pour affichage
import getSensors_atlas # pour récupérer les valeurs des lectures Atlas
import getSensors_ds18b20 # pour récupérer les valeurs des lecture 1-Wire
import syst_config # fichier constantes <syst_config.py>
import syst_logique
import publish_ThingSpeak as status

def initLabel(pRoot, pText, pWidth, pFg, pPosX, pPosY):
    ''' Permet d'initialiser un objet tkinter label de titre.
        @param On prend en paramètres la référence de l'objet tkinter, le texte à afficher,
        la longueur du label (s'ajuste au nombre de caractères dans la string), la couleur 
        du texte, la position X,Y de l'obejet label.  
        @return Retourne l'objet créé.
    '''
    label = tk.Label(pRoot, text=pText, bg=syst_config.TKI_BACKCOLOR, font=(syst_config.TKI_FONT,syst_config.TKLEN_LBL), width=pWidth, fg=pFg) # création du label, set les paramètres
    label.place(relx=pPosX, rely=pPosY) # position
    
    return label # retourne l'objet pour la référence

def initLabelValue(pRoot, pWidth, pPosX, pPosY):
    ''' Permet d'initialiser un objet tkinter label d'une valeur variable.
        @param On prend en paramètres la référence de l'objet tkinter, la 
        longueur du label (s'ajuste au nombre de caractères dans la string)
        et la position X,Y de l'obejet label.  
        @return Retourne l'objet créé.
    '''
    labelValue = tk.Label(pRoot, bg=syst_config.TKI_BACKCOLOR, font=(syst_config.TKI_FONT,syst_config.TKLEN_VAR), width=pWidth, fg=syst_config.TKI_TEXTCOLOR) # création du label, set les paramètres
    labelValue.place(relx=pPosX, rely=(pPosY+syst_config.TKPOS_OFFSET)) # position du label value
    labelValue.config(text=syst_config.TKI_NULLMESSAGE) # message initial/null

    return labelValue # retourne l'objet pour la référence

def genAfficheCRIFA():
    ''' Permet de générer l'affichage pour une serre sans capteurs à eau. Affiche les
        résultats de CO², d'Humidité, de Température Atlas et des capteurs de température
        des DS18B20.
    '''
    global root
    global lblInternet
    global lblHUM
    global lblCO2
    global lblDS1
    global lblDS2
    global lblDS3
    global lblDS4
    global lblMOY

    # POS COLONNE LEFT
    # CO²
    initLabel(root, "CO² (ppm)", 9, "orange", syst_config.TKPOS_LEFT, syst_config.TKPOS_TOP) # text, width, couleur, pos x,y
    lblCO2 = initLabelValue(root, 6, syst_config.TKPOS_LEFT, syst_config.TKPOS_TOP + syst_config.TKPOS_OFFSET) # width, pos x,y 
    
    # HUMIDITÉ
    initLabel(root, "Humidité (%)", 12, "cyan", syst_config.TKPOS_LEFT, syst_config.TKPOS_MIDDLE + syst_config.TKPOS_TOP) # text, width, couleur, pos x,y
    lblHUM = initLabelValue(root, 6, syst_config.TKPOS_LEFT, syst_config.TKPOS_MIDDLE + syst_config.TKPOS_TOP + syst_config.TKPOS_OFFSET) # width, pos x,y 
    
    # connection internet
    initLabel(root, "Connection status", 17, "red", syst_config.TKPOS_LEFT, syst_config.TKPOS_BOTTOM) # text, width, couleur, pos x,y
    lblInternet = initLabelValue(root, 6, syst_config.TKPOS_LEFT, syst_config.TKPOS_BOTTOM + syst_config.TKPOS_OFFSET) # width, pos x,y

    # Moyenne temperature
    initLabel(root, "Temp. MOY (°C)", 14, "orange", syst_config.TKPOS_CENTER, syst_config.TKPOS_TOP) # text, width, couleur, pos x,y
    lblMOY = initLabelValue(root, 6, syst_config.TKPOS_CENTER, syst_config.TKPOS_TOP + syst_config.TKPOS_OFFSET) # width, pos x,y 

    # CAPTEURS DS18B20
    # POS COLONNE CENTER
    # DS1
    initLabel(root, "Temp. D1 (°C)", 13, "magenta", syst_config.TKPOS_CENTER, syst_config.TKPOS_MIDDLE + syst_config.TKPOS_TOP) # text, width, couleur, pos x,y
    lblDS1 = initLabelValue(root, 6, syst_config.TKPOS_CENTER, syst_config.TKPOS_MIDDLE + syst_config.TKPOS_TOP + syst_config.TKPOS_OFFSET) # width, pos x,y 
    
    # DS2
    initLabel(root, "Temp. D2 (°C)", 13, "magenta", syst_config.TKPOS_CENTER, syst_config.TKPOS_BOTTOM) # text, width, couleur, pos x,y
    lblDS2 = initLabelValue(root, 6, syst_config.TKPOS_CENTER, syst_config.TKPOS_BOTTOM + syst_config.TKPOS_OFFSET) # width, pos x,y 
    
    # POS COLONNE RIGHT
    # DS3
    initLabel(root, "Temp. D3 (°C)", 13, "magenta", syst_config.TKPOS_RIGHT, syst_config.TKPOS_MIDDLE + syst_config.TKPOS_TOP) # text, width, couleur, pos x,y
    lblDS3 = initLabelValue(root, 6, syst_config.TKPOS_RIGHT, syst_config.TKPOS_MIDDLE + syst_config.TKPOS_TOP + syst_config.TKPOS_OFFSET) # width, pos x,y 
    
    # DS4
    initLabel(root, "Temp. D4 (°C)", 13, "magenta", syst_config.TKPOS_RIGHT, syst_config.TKPOS_BOTTOM) # text, width, couleur, pos x,y
    lblDS4 = initLabelValue(root, 6, syst_config.TKPOS_RIGHT, syst_config.TKPOS_BOTTOM + syst_config.TKPOS_OFFSET) # width, pos x,y

    # img = ImageTk.PhotoImage(Image.open("CRIFA.png"))    
    # panel = tk.Label(root, image = img)
    # #panel.place(relx=syst_config.TKPOS_CENTER, rely=(syst_config.TKPOS_TOP+syst_config.TKPOS_OFFSET))
    # panel.pack(side = "bottom", fill = "both", expand = "yes")


def initAffichage():
    ''' Initialise la page principale de l'affichage. Création de la 
        fenêtre et initialisation des objets.
        @return Retourne la référence de l'objet tkinter pour les autres
        fichiers qui l'utilise.
    '''
    # identification des variables globales de la fonction
    global root
    #global panel

    print("Initialisation de l'affichage.")
    
    # Création de la fenêtre
    root = tk.Tk() # obj tkinter
    root.title("Serrebrooke")   # titre de la page
    root.config(bg = syst_config.TKI_BACKCOLOR) # couleur de fond de la fenêtre
    root.geometry(syst_config.TKI_RESOLUTION)   # dimension de l'écran, résolution de la fenêtre
    root.attributes("-fullscreen",syst_config.TKI_FULLSCREEN)   # mode plein écran, init = true
    
    genAfficheCRIFA()
    return root # retourne la variable globale pour référencer à d'autres fichiers

def getValues():
    ''' Permet de récupérer les valeurs des capteurs et de les afficher sur l'application
        si les capteurs sont actifs. La gestion des valeurs se fait dans les fichiers 
        getSensors respectifs.
    '''
    global root
    global lblTemp
    global lblHUM
    global lblCO2
    global lblDS1
    global lblDS2
    global lblDS3
    global lblDS4
    global lblMOY
    # raffraichit les valeurs des capteurs DS18B20
    # raffraîchit les valeurs 
    # essaie de récupérer la valeur.
    # si le capteur est inexistant, une exception est lancée, donc on affiche
    # à la place "----" pour indiquer qu'il est absent. 
    try:
        lblDS1.config(text=str(getSensors_ds18b20.temp1))
    except:
        lblDS1.config(text='----')
    try:
        lblDS2.config(text=str(getSensors_ds18b20.temp2))
    except:
        lblDS2.config(text='----')
    try:
        lblDS3.config(text=str(getSensors_ds18b20.temp3))
    except:
        lblDS3.config(text='----')
    try:
        lblDS4.config(text=str(getSensors_ds18b20.temp4))
    except:
        lblDS4.config(text='----')
    try:
        lblMOY.config(text=str(getSensors_ds18b20.tempMOY))
    except:
        lblMOY.config(text='----')

    try:
        if getSensors_atlas.humVal != -1:
            lblHUM.config(text=str(getSensors_atlas.humVal))
        else:
            raise Exception()
    except:
        lblHUM.config(text='----')
    
    try:
        lblInternet.config(text=(status.connectionStatus))   
    except:
        lblInternet.config(text='----')
    
    try:
        if getSensors_atlas.co2Val != -1:
            lblCO2.config(text=str(getSensors_atlas.co2Val))
        else:
            raise Exception()
    except:
        lblCO2.config(text='----')

            
def tkiAffiche(pRoot, pValues:bool=True):
    ''' Permet de gérer la récupération des valeurs si valide et
        de référencer l'objet tkinter pour les autres fichiers.
        Raffraîchit l'affichage.
        @param On prend en paramètres la référence de l'objet tkinter
        et la validation pour récuprérer les valeurs des capteurs.
    '''
    global root
    root = pRoot
    if(pValues):
        getValues()        

    #root.update_idletasks()
    #root.mainloop()
    root.update()

''' Boucle programme principale, si appelé comme fichier main.
    Permet de générer l'affichage et d'attendre le keyboard interrupt.
'''
if __name__ == '__main__':
    
    print('Départ du programme en main()...')
    root = initAffichage()
    print('Initialisation de l\'affichage...')
    try:
        while(1): 
            tkiAffiche(False, root) # boucle qui raffraîchit l'affichage
            sleep(syst_config.tkiDelay)
    except KeyboardInterrupt:
        print('\nProgramme interrompu. Fin du programme.')
        root.destroy # détruit l'affichage avant de quitter
        exit # quitte le programme


# divers....
# #lable temps delai selec
# labelT = tk.Label(root, text="delai " + str(delaiMesure/60) + "minute(s)", bg = couleurB, fg =couleurT, width=25)# couleurB fond et text du lable
# labelT.place(relx=centre, rely=bas)#bouton en bas
