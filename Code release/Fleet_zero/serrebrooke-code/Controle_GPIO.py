from flask import Flask, render_template_string, request, jsonify
import RPi.GPIO as GPIO
from datetime import datetime



app = Flask(__name__)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ports = [20, 21, 18, 23, 24, 25, 26, 14, 15, 16, 17, 27, 22, 19]
for port in ports:
    GPIO.setup(port, GPIO.OUT)

def get_gpio_status():
    status = {}
    for port in ports:
        status[port] = GPIO.input(port)
    return status

@app.route('/')
def index():
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
                            display += `Port ${port}: ${status ? 'ON' : 'OFF'}<br>`;
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

            setInterval(refreshStatus, 1000);  // Refresh every 1000 milliseconds
        </script>
    </head>
    <body onload="refreshStatus()">
        <h1>Contrôle des ports GPIO du Raspberry Pi</h1>

        <!-- GPIO Status Display -->
        <div id="status"></div>

        <form onsubmit="return sendToggle()">
            <label for="port">Numéro du port GPIO :</label>
            <input type="text" id="port" name="port" required><br><br>

            <label for="name">Nom:</label>
            <input type="text" id="name" name="name"><br><br>

            <input type="radio" id="on" name="action" value="ON" required>
            <label for="on">ON</label><br>

            <input type="radio" id="off" name="action" value="OFF" required>
            <label for="off">OFF</label><br><br>

            <input type="submit" value="Changement">
        </form>

        <div id="log"></div>
    </body>
    </html>
    """)

@app.route('/status')
def status():
    return jsonify(get_gpio_status())

@app.route('/toggle', methods=['POST'])
def toggle():
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
            return jsonify({"port": port, "action": action, "name": name, "timestamp": timestamp})
    return jsonify({"error": "Invalid request"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

