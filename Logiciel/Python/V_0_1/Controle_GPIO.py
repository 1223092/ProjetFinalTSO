# Andy Flores
# Date: 2023-12-18
# Résumé: Ce script Python utilise Flask pour créer une application web permettant de contrôler et de suivre l'état des ports GPIO d'un Raspberry Pi.

from flask import Flask, render_template_string, request, jsonify, send_file
import RPi.GPIO as GPIO  # Importe la bibliothèque pour contrôler les GPIO sur Raspberry Pi
from datetime import datetime # Importe la bibliothèque pour le temps
# Importe les bibliothèque pour les 3 types de fichier
import json
import csv
import xml.etree.ElementTree as ET


app = Flask(__name__)  # Création d'une instance de l'application Flask

# Configuration initiale des ports GPIO
GPIO.setmode(GPIO.BCM)  # Utilisation de la numérotation BCM pour les ports GPIO
GPIO.setwarnings(False)  # Désactivation des avertissements GPIO
ports = [20, 21, 18, 23, 24, 25, 26, 14, 15, 16, 17, 27, 22, 19]  # Liste des ports GPIO utilisés
for port in ports:
    GPIO.setup(port, GPIO.OUT)  # Configure chaque port en mode sortie

log_entries = []  # Liste pour stocker les entrées de journalisation

def get_gpio_status():
    """ Récupère l'état actuel de tous les ports GPIO. """
    status = {}
    for port in ports:
        status[port] = GPIO.input(port)  # Lit l'état de chaque port
    return status

def log_to_file():
    """ Enregistre les entrées du journal dans différents formats de fichier. """
    with open('log.json', 'w') as json_file:
        json.dump(log_entries, json_file)  # Enregistrement au format JSON
    with open('log.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['timestamp', 'name', 'port', 'action'])  # En-têtes CSV
        for entry in log_entries:
            writer.writerow([entry['timestamp'], entry['name'], entry['port'], entry['action']])  # Écriture des entrées CSV
    with open('log.xml', 'w') as xml_file:
        root = ET.Element('log')
        for entry in log_entries:
            child = ET.SubElement(root, 'entry')
            for key, value in entry.items():
                ET.SubElement(child, key).text = str(value)  # Création des éléments XML
        tree = ET.ElementTree(root)
        tree.write(xml_file)  # Enregistrement au format XML

@app.route('/')
def index():
    """ Route pour la page d'accueil. Affiche l'interface utilisateur pour le contrôle des GPIO. """
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Contrôle GPIO Raspberry Pi</title>
        <script>
            function refreshStatus() {
                fetch('/status')
                    .then(response => response.json())
                    .then(data => {
                        let display = '';
                        for (const [port, status] of Object.entries(data)) {
                            const color = status ? 'green' : 'red';
                            display += `Port ${port}: <span style="color: ${color};">${status ? 'ON' : 'OFF'}</span><br>`;
                        }
                        document.getElementById('status').innerHTML = display;
                    });
            }

            function sendToggle() {
                const port = document.getElementById('port').value;
                const action = document.querySelector('input[name="action"]:checked').value;
                const name = document.getElementById('name').value || 'inconnu';

                fetch('/toggle', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `port=${port}&action=${action}&name=${name}`
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.error) {
                        const logEntry = `${data.timestamp}: ${data.name} turned port ${data.port} ${data.action === 'ON' ? '<span style="color: green;">ON</span>' : '<span style="color: red;">OFF</span>'}<br>`;
                        document.getElementById('log').innerHTML += logEntry;
                    }
                });
                return false; // Prevent form from submitting normally
            }

            function refreshLog() {
                fetch('/log')
                    .then(response => response.json())
                    .then(data => {
                        let logDisplay = '';
                        data.forEach(entry => {
                            const color = entry.action === 'ON' ? 'green' : 'red';
                            logDisplay += `${entry.timestamp}: ${entry.name} turned port ${entry.port} <span style="color: ${color};">${entry.action}</span><br>`;
                        });
                        document.getElementById('log').innerHTML = logDisplay;
                    });
            }

            setInterval(refreshStatus, 1000);  // Refresh every 1000 milliseconds
            setInterval(refreshLog, 1000);     // Refresh log every 1000 milliseconds
        </script>
    </head>
    <body onload="refreshStatus(); refreshLog();">
        <h1>Contrôle des ports GPIO du Raspberry Pi</h1>

        <!-- Affichage de l'état des GPIO -->
        <div id="status"></div>

        <!-- Formulaire pour changer l'état des GPIO -->
        <form onsubmit="return sendToggle()">
            <label for="port">Numéro du port GPIO :</label>
            <input type="text" id="port" name="port" required><br><br>

            <label for="name">Nom:</label>
            <input type="text" id="name" name="name"><br><br>

            <input type="radio" id="on" name="action" value="ON" required>
            <label for="on">ON</label><br>

            <input type="radio" id="off" name="action" value="OFF" required>
            <label for="off">OFF</label><br><br>

            <input type="submit" value="Toggle">
        </form>

        <!-- Affichage du journal des actions -->
        <div id="log"></div>

        <!-- Boutons pour télécharger le journal en différents formats -->
        <button onclick="window.location.href='/download/json'">Télécharger JSON</button>
        <button onclick="window.location.href='/download/xml'">Télécharger XML</button>
        <button onclick="window.location.href='/download/csv'">Télécharger CSV</button>
    </body>
    </html>
    """)

@app.route('/status')
def status():
    """ Route pour obtenir l'état actuel des GPIO. """
    return jsonify(get_gpio_status())

@app.route('/log')
def log():
    """ Route pour obtenir le journal des actions. """
    return jsonify(log_entries)

@app.route('/toggle', methods=['POST'])
def toggle():
    """ Route pour changer l'état d'un port GPIO. """
    port = request.form.get('port')
    action = request.form.get('action')
    name = request.form.get('name') or "inconnu"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if port and action:
        port = int(port)
        if port in ports:
            if action == 'ON':
                GPIO.output(port, GPIO.HIGH)
            elif action == 'OFF':
                GPIO.output(port, GPIO.LOW)
            entry = {"timestamp": timestamp, "name": name, "port": port, "action": action}
            log_entries.append(entry)
            log_to_file()
            return jsonify(entry)
    return jsonify({"error": "Invalid request"})

@app.route('/download/<filetype>')
def download_log(filetype):
    """ Route pour télécharger le journal des actions dans différents formats. """
    if filetype in ['json', 'csv', 'xml']:
        return send_file(f'log.{filetype}', as_attachment=True)
    return jsonify({"error": "Invalid file type"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Exécute l'application sur le port 80
