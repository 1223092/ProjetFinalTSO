function toggleTimerControl(enabled) {
    document.getElementById('timerOn').disabled = !enabled;
    document.getElementById('timerOff').disabled = !enabled;
    // Disable the other switches when timer is activated
    document.getElementById('activerVent').disabled = enabled;
    document.getElementById('activerHumidity').disabled = enabled;
    if (enabled) {
        document.getElementById('activerVent').checked = false;
        document.getElementById('activerHumidity').checked = false;
        toggleVentilationControl(false);
        toggleHumidityControl(false);
    }
}

function toggleTemperatureSection(enabled) {
    document.getElementById('temperatureValue').disabled = !enabled;
}

function toggleHumidificateurSection(enabled) {
    document.getElementById('humidificateurValue').disabled = !enabled;
}
function toggleHumidityControl(enabled) {
    document.getElementById('humidityValue').disabled = !enabled;
    // Disable timer switch when this is activated
    document.getElementById('activateTimer').disabled = enabled;
    if (enabled) {
        document.getElementById('activateTimer').checked = false;
        toggleTimerControl(false);
    }
}

function toggleHumidificateurSchedule(enabled) {
    document.getElementById('secondHumidificateurValue').disabled = !enabled;
    document.getElementById('humidificateurStartTime').disabled = !enabled;
    document.getElementById('humidificateurEndTime').disabled = !enabled;
}

function setHumidificateur() {
    var humidity = document.getElementById('humidificateurValue').value;
    fetch('/set_humidificateur', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ humidity: humidity }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('currentHumidificateur').textContent = humidity;
    })
    .catch(error => console.error('Error:', error));
}

function fetchCurrentHumidificateur() {
    fetch('/get_current_humidificateur')
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentHumidificateur').textContent = data.humidity || 'NA';
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById('programming-tab').addEventListener('click', fetchCurrentHumidificateur);

function toggleSecondTemperatureSection(enabled) {
    document.getElementById('secondTemperatureValue').disabled = !enabled;
    document.getElementById('heatingStartTime').disabled = !enabled;
    document.getElementById('heatingEndTime').disabled = !enabled;
}

function toggleHumidityInput(enabled) {
    document.getElementById('humidityValue').disabled = !enabled;
}

function toggleVentilationSection(enabled) {
    document.getElementById('humidityValue2').disabled = !enabled;
    document.getElementById('ventilationStartTime').disabled = !enabled;
    document.getElementById('ventilationEndTime').disabled = !enabled;
}

function toggleVentilationControl(enabled) {
    document.getElementById('activateTimer').disabled = enabled;
    document.getElementById('humidityValue2').disabled = !enabled;
    document.getElementById('ventilationStartTime').disabled = !enabled;
    document.getElementById('ventilationEndTime').disabled = !enabled;
    if (enabled) {
        document.getElementById('activateTimer').checked = false;
        toggleTimerControl(false);
    }
}

function toggleLightSection(enabled) {
    document.getElementById('lightStartTime').disabled = !enabled;
    document.getElementById('lightEndTime').disabled = !enabled;
}

function updateGraph(results, chartId, chartNumber = 1) {
    var src = `https://thingspeak.com/channels/1328019/charts/${chartNumber}?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=${results}&title=Température+D${chartNumber}&type=line&xaxis=Time&yaxis=Température&yaxismax=40&yaxismin=5`;
    document.getElementById(chartId).src = src;
}

function updateEnvironmentalGraph(results, chartId, chartNumber) {
    let title, yAxisUnit, yAxisMax;
    if (chartNumber === 6) {  // CO2 graph specific parameters
        title = "CO²";
        yAxisUnit = "PPM";
        yAxisMax = 1000;
    } else if (chartNumber === 7) {  // Humidity graph specific parameters
        title = "Humidité";
        yAxisUnit = "%25";  // Encoded "%" for URL
        yAxisMax = 100;
    }

    var src = `https://thingspeak.com/channels/1328019/charts/${chartNumber}?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=${results}&title=${title}&type=line&xaxis=Time&yaxis=${yAxisUnit}&yaxismax=${yAxisMax}&yaxismin=0`;
    document.getElementById(chartId).src = src;
}

function setHumidity() {
    var humidity = document.getElementById('humidityValue').value;
    fetch('/set_humidity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ humidity: humidity }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('currentHumidity').textContent = humidity;
    })
    .catch(error => console.error('Erreur:', error));
}

function clearHumidity() {
    fetch('/clear_humidity', {
        method: 'POST',
    })
    .then(response => {
        document.getElementById('currentHumidity').textContent = 'NA';
        document.getElementById('humidityValue').value = '';
    })
    .catch(error => console.error('Erreur:', error));
}

function fetchCurrentHumidity() {
    fetch('/get_current_humidity')
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentHumidity').textContent = data.humidity || 'NA';
        })
        .catch(error => console.error('Erreur:', error));
}

function setSchedule(device) {
    var start = document.getElementById(device + 'StartTime').value;
    var end = document.getElementById(device + 'EndTime').value;
    fetch('/set_schedule/' + device, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start: start, end: end }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Schedule set:', data);
    })
    .catch(error => console.error('Error:', error));
}

function fetchDeviceStates() {
    updateStateIcon('10.42.0.29', 'chauffageIcon');
    updateStateIcon('10.42.0.130', 'lumiereIcon');
    updateStateIcon('10.42.0.88', 'ventilationIcon');
    updateStateIcon('10.42.0.85', 'humidificateurIcon');
}

function updateStateIcon(ip, elementId) {
    fetch(`/state/${ip}`)
        .then(response => response.json())
        .then(data => {
            let icon = '🔴';
            if (data.state === 'ON') {
                icon = '🟢';
            } else if (data.state === 'OFF') {
                icon = '🔴';
            }
            document.getElementById(elementId).textContent = icon;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById(elementId).textContent = '⚫';
        });
}

function fetchAverageTemperature() {
    fetch('/get_average_temperature')
        .then(response => response.json())
        .then(data => {
            document.getElementById('averageTemperature').textContent = data.average_temperature.toFixed(1);
        })
        .catch(error => console.error('Error fetching average temperature:', error));
}

function fetchLatestHumidity() {
    fetch('/get_humidity')
        .then(response => response.json())
        .then(data => {
            document.getElementById('latestHumidity').textContent = data.humidity;
        })
        .catch(error => console.error('Error fetching humidity:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    fetchAverageTemperature();
    fetchLatestHumidity();
    fetchDeviceStates();
});

function clearSchedule(device) {
    fetch('/clear_schedule/' + device, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Schedule cleared:', data);
        document.getElementById(device + 'StartTime').value = '';
        document.getElementById(device + 'EndTime').value = '';
    })
    .catch(error => console.error('Error:', error));
}

function fetchSchedule(device) {
    fetch('/get_schedule/' + device)
        .then(response => response.json())
        .then(data => {
            if (data.start !== 'NA') {
                document.getElementById(device + 'StartTime').value = data.start;
            }
            if (data.end !== 'NA') {
                document.getElementById(device + 'EndTime').value = data.end;
            }
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById('programming-tab').addEventListener('click', function() {
    fetchDeviceStates();
    fetchSchedule('lumiere');
    fetchSchedule('chauffage');
    fetchSchedule('ventilation');
});

document.getElementById('programming-tab').addEventListener('click', fetchCurrentHumidity);

function fetchCurrentTemperature() {
    fetch('/get_current_temperature')
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentTemperature').textContent = data.temperature || 'NA';
        })
        .catch(error => console.error('Erreur:', error));
}

document.getElementById('programming-tab').addEventListener('click', fetchCurrentTemperature);

function setTemperature() {
    var temperature = document.getElementById('temperatureValue').value;
    fetch('/set_temperature', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ temperature: temperature }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('currentTemperature').textContent = temperature;
    })
    .catch(error => console.error('Erreur:', error));
}

function clearTemperature() {
    fetch('/clear_temperature', {
        method: 'POST',
    })
    .then(response => {
        document.getElementById('currentTemperature').textContent = 'NA';
        document.getElementById('temperatureValue').value = '';
    })
    .catch(error => console.error('Erreur:', error));
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function toggleNightMode() {
    var body = document.body;
    body.classList.toggle("night-mode");
    var button = document.getElementById("nightModeButton");
    if (body.classList.contains("night-mode")) {
        button.textContent = "Light Mode";
        body.style.backgroundColor = "#333";
        body.style.color = "#fff";
    } else {
        button.textContent = "Night Mode";
        body.style.backgroundColor = "#fff";
        body.style.color = "#000";
    }
}

function saveSettings() {
    var settings = {
        chauffage: {
            active: document.getElementById('activerTemp').checked,
            value: parseFloat(document.getElementById('temperatureValue').value),
            schedule_active: document.getElementById('activerSecondTemp').checked,
            schedule: {
                start: document.getElementById('heatingStartTime').value,
                end: document.getElementById('heatingEndTime').value
            },
            value2: parseFloat(document.getElementById('secondTemperatureValue').value),
            tempDeadband: parseFloat(document.getElementById('tempDeadband').value)
        },
        ventilation: {
            active: document.getElementById('activerHumidity').checked,
            humidity: parseFloat(document.getElementById('humidityValue').value),
            schedule_active: document.getElementById('activerVent').checked,
            schedule: {
                start: document.getElementById('ventilationStartTime').value,
                end: document.getElementById('ventilationEndTime').value
            },
            humidity2: parseFloat(document.getElementById('humidityValue2').value),
            ventDeadband: parseFloat(document.getElementById('ventDeadband').value),
            timerOn: parseInt(document.getElementById('timerOn').value),
            timerOff: parseInt(document.getElementById('timerOff').value),
            timerActive: document.getElementById('activateTimer').checked
        },
        humidificateur: {
            active: document.getElementById('activateHumidificateur').checked,
            humidity: parseFloat(document.getElementById('humidificateurValue').value),
            schedule_active: document.getElementById('activateHumidificateurSchedule').checked,
            schedule: {
                start: document.getElementById('humidificateurStartTime').value,
                end: document.getElementById('humidificateurEndTime').value
            },
            humidity2: parseFloat(document.getElementById('secondHumidificateurValue').value),
            humDeadband: parseFloat(document.getElementById('humDeadband').value)
        },
        lumiere: {
            active: document.getElementById('activerLight').checked,
            schedule: {
                start: document.getElementById('lightStartTime').value,
                end: document.getElementById('lightEndTime').value
            }
        }
    };

    fetch('/save_all_settings', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => alert('Settings saved successfully!'))
    .catch(error => console.error('Error saving settings:', error));
}

function toggleDeviceState(device, elementId) {
    fetch(`/action/${device.toLowerCase()}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ip: DEVICE_IPS[device] })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(elementId).textContent = data.state;
    })
    .catch(error => console.error('Error:', error));
}

window.onload = function() {
    openTab(event, 'Dashboard');
};

function setTemperature() {
    var temperature = document.getElementById('temperatureValue').value;
    fetch('/set_setting', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({temperature: temperature})
    }).then(response => response.json())
    .then(data => {
        console.log('Temperature updated', data);
    }).catch(error => console.error('Error updating temperature:', error));
}

function updateUIWithSettings() {
    fetch('/get_settings')
        .then(response => response.json())
        .then(data => {
            document.getElementById('activerTemp').checked = data.chauffage.active;
            document.getElementById('temperatureValue').value = data.chauffage.value || '';
            document.getElementById('activerSecondTemp').checked = data.chauffage.schedule_active;
            document.getElementById('secondTemperatureValue').value = data.chauffage.value2 || '';
            document.getElementById('heatingStartTime').value = data.chauffage.schedule.start || '';
            document.getElementById('heatingEndTime').value = data.chauffage.schedule.end || '';

            document.getElementById('ventDeadband').value = data.ventilation.ventDeadband || '';
            document.getElementById('activerHumidity').checked = data.ventilation.active;
            document.getElementById('humidityValue').value = data.ventilation.humidity || '';
            document.getElementById('activerVent').checked = data.ventilation.schedule_active;
            document.getElementById('humidityValue2').value = data.ventilation.humidity2 || '';
            document.getElementById('ventilationStartTime').value = data.ventilation.schedule.start || '';
            document.getElementById('ventilationEndTime').value = data.ventilation.schedule.end || '';
            document.getElementById('timerOn').value = data.ventilation.timerOn || 0;
            document.getElementById('timerOff').value = data.ventilation.timerOff || 0;
            document.getElementById('activateTimer').checked = data.ventilation.timerActive;

            toggleTimerControl(data.ventilation.timerActive);
            toggleVentilationControl(data.ventilation.schedule_active);

            document.getElementById('tempDeadband').value = data.chauffage.tempDeadband || '';
            document.getElementById('activateHumidificateur').checked = data.humidificateur.active;
            document.getElementById('humidificateurValue').value = data.humidificateur.humidity || '';
            document.getElementById('activateHumidificateurSchedule').checked = data.humidificateur.schedule_active;
            document.getElementById('secondHumidificateurValue').value = data.humidificateur.humidity2 || '';
            document.getElementById('humidificateurStartTime').value = data.humidificateur.schedule.start || '';
            document.getElementById('humidificateurEndTime').value = data.humidificateur.schedule.end || '';

            document.getElementById('humDeadband').value = data.humidificateur.humDeadband || '';
            document.getElementById('activerLight').checked = data.lumiere.active;
            document.getElementById('lightStartTime').value = data.lumiere.schedule.start || '';
            document.getElementById('lightEndTime').value = data.lumiere.schedule.end || '';
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById('programming-tab').addEventListener('click', updateUIWithSettings);
window.onload = updateUIWithSettings;

function fetchTemperature() {
    fetch('/get_setting/temperature')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperatureValue').value = data.temperature || '';
        }).catch(error => console.error('Error fetching temperature:', error));
}

document.getElementById('temperatureUpdateButton').addEventListener('click', setTemperature);
window.onload = fetchTemperature;

function fetchState(ip, elementId) {
    fetch(`/state/${ip}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let displayState = 'N/A'; // Default state
            if (data.state && (data.state === 'ON' || data.state === 'OFF')) {
                displayState = data.state;
            }
            document.getElementById(elementId).textContent = displayState;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById(elementId).textContent = 'N/A';
        });
}

document.getElementById('control-tab').addEventListener('click', updateStates);
