from flask import Flask, render_template_string, request
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuration des GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ports = [17, 27, 22]  # Exemple de numéros de ports GPIO
for port in ports:
    GPIO.setup(port, GPIO.OUT)

@app.route('/')

def index():
    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Contrôle GPIO Raspberry Pi</title>
    </head>
    <body>
        <h1>Contrôle des ports GPIO du Raspberry Pi</h1>

        <form action="/toggle" method="post">
            <label for="port">Numéro du port GPIO :</label>
            <input type="text" id="port" name="port" required><br><br>

            <input type="submit" name="action" value="ON">
            <input type="submit" name="action" value="OFF">
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

def index():
    return render_template('index.html')  # Assurez-vous d'avoir un template index.html

@app.route('/toggle', methods=['POST'])
def toggle():
    port = request.form.get('port')
    action = request.form.get('action')
    
    if port and action:
        port = int(port)
        if port in ports:
            if action == 'ON':
                GPIO.output(port, GPIO.HIGH)
            elif action == 'OFF':
                GPIO.output(port, GPIO.LOW)
            return f"Port {port} turned {action}"
    return "Invalid request"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001
)
