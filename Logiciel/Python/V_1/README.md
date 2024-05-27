# V_2
<p>Programme pour le projet Serrebrooke.<p>
<p>Version 2.0<p>
<p>7 mai 2024<p>
<p>Andy Van Flores Gomez et Loïc Sarhy<p>

## Resume
<p> Programme qui permet de recolter des données de différents appareils de mesures, généralement
    installé dans une serre. Celles-ci sont envoyés par MQTT et récoltés par la plateforme Thingspeak
    qui agit comme broker. Le programme déploye aussi une page web à partir de laquelle des consignes
    peuvent être choisi afin de controler les différents instruments HVAC qui permet d'avoir les
    conditions demanés à l'intérieur de l'environment ou le système est installé.
</p>

## Matériel
### Fichiers
<ul>
<li>boucle_finale.py</li>
<li>getSensors_atlas.py</li>
<li>getSensors_ds18b20.py</li>
<li>publish_ThingSpeak.py</li>
<li>publish_UDP.py</li>
<li>site_final.py</li>
<li>syst_config.py</li>
<li>syst_interface.py</li>
<li>syst_logique.py</li>
</ul>

### Environnement
<ul>
<li>Utilisation de l'éditeur VScode pour le développement en python.</li>
<li>Interpreteur python.</li>
<li>Déployer dans un RaspberriePI</li>
<li>Déployer via un conteneur Balena</li>
</ul>

## Utilisation
<ul> 
    <li>S'assurer d'avoir les fichiers dans le même répertoire.</li>
    <li>Ouvrir et démarrer le fichier syst_logique.py.</li>
    <li>Les instructions sur les touches disponibles se trouve au début du fichier carrier.py </li>
</ul>
<p>Le fichier va démarrer la prise de mesures de capteurs, affichage à l'écran local, l'envoie des données par
    MQTT et la page web. Cette dernière sera accessible via un URL disponible par Balena.
</p>