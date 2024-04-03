'''
    @file       syst_config.py
    @date       Avril 2022
    @version    0.2
                Adaptation pour code NFT
    @brief      Fichier des variables, contantes, etc. configurables.
                Permet de modifier les valeurs sans affecter la logique du code.
    @Auteurs    Andy Van Flores Gonzalez, Loïc Sarhy
    @compilateur interpreteur Python
'''


# Fréquence d'acquisition
tkiDelay = 2 # délai par défaut de l'aquisition des mesures
tsDelay = 5 # delai d'intervalle au minutes pour envoyer les donnees sur thingspeak

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