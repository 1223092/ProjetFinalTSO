import requests
import getSensors_ds18b20 
import getSensors_atlas 
from datetime import datetime
import time
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEATER_URL = "http://10.42.0.23/cm?cmnd=Power%20"
VENTILATION_URL = "http://10.42.0.88/cm?cmnd=Power%20"
LUMIERE_URL = "http://10.42.0.130/cm?cmnd=Power%20"

def read_set_value(filename):
    try:
        with open(filename, 'r') as file:
            value = file.read().strip()
            return float(value) if value else None
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return None

def read_schedule(filename):
    try:
        with open(filename, 'r') as file:
            times = file.read().strip().split(',')
            if len(times) == 2:
                start = datetime.strptime(times[0], '%H:%M').time()
                end = datetime.strptime(times[1], '%H:%M').time()
                return (start, end) if start and end else (None, None)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return None, None
    return None, None

def check_within_schedule(start, end):
    now = datetime.now().replace(second=0, microsecond=0).time()
    print(now)
    return start <= now <= end

def control_device(url, condition):
    requests.get(f"{url}{'on' if condition else 'off'}")
    

def control_heating(temp_set, current_temp, heater_schedule):
    start, end = heater_schedule
    if start and end:
        if check_within_schedule(start, end):  
            if temp_set is not None:
                if current_temp < temp_set - 1:
                    requests.get(f"{HEATER_URL}on")
                elif current_temp > temp_set + 1:
                    requests.get(f"{HEATER_URL}off")
            

def control_ventilation(hum_set, current_hum, ventilation_schedule):
    start, end = ventilation_schedule
    if start and end:
        condition = hum_set is not None and current_hum > hum_set + 3
        control_device(VENTILATION_URL, condition and check_within_schedule(start, end))

def control_lumiere(lumiere_schedule):
    start, end = lumiere_schedule
    if start and end:
        control_device(LUMIERE_URL, check_within_schedule(start, end))

def main():
    while True:
        
        temp = getSensors_ds18b20.getDS18B20()
        tempmoy = temp[-1]  
        
        getSensors_atlas.getAtlas()
        humVal = float(getSensors_atlas.humVal)

        temp_set = read_set_value("temp_set.txt")
       
        hum_set = read_set_value("hum_set.txt")

        heater_schedule = read_schedule('chauffage_schedule.txt')
        
        ventilation_schedule = read_schedule('ventilation_schedule.txt')
        
        lumiere_schedule = read_schedule('lumiere_schedule.txt')

        control_heating(temp_set, tempmoy, heater_schedule)
        control_ventilation(hum_set, humVal, ventilation_schedule)
        control_lumiere(lumiere_schedule)
        print(f"Current Temp: {tempmoy}, Set Temp: {temp_set}, Schedule: {heater_schedule}")

        time.sleep(2)

if __name__ == "__main__":
    main()
