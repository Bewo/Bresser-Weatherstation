from bottle import request, response, route, run
import datetime, json, os
import paho.mqtt.client as mqtt

# MQTT-Konfiguration über Umgebungsvariablen
MQTT_HOST = os.getenv('MQTT_HOST', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_USER = os.getenv('MQTT_USER', '')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', '')
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'wetterstation/data')

print(f"Verbinde zu {MQTT_HOST}:{MQTT_PORT} mit User {MQTT_USER}…")

current_data = {}

WIND_DIRS = [
    'N', 'NNE', 'NE', 'ENE',
    'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW',
    'W', 'WNW', 'NW', 'NNW'
]

def deg_to_dir(deg):
    return WIND_DIRS[round(int(deg) / 22.5) % 16]

def mph_to_kmh(mph):
    return round(float(mph) * 1.609344, 1)

def mph_to_ms(mph):
    return round(float(mph) * 0.44704, 1)

def in_to_mm(inches):
    return round(float(inches) * 25.4, 1)

def f_to_c(tempf):
    return round((float(tempf) - 32) * 5 / 9, 1)

def min_to_hpa(pressuremin):
    return round(float(pressuremin) * 33.7685)

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[INFO] Verbunden mit MQTT Broker {MQTT_HOST}:{MQTT_PORT} mit Resultcode {rc}")

# MQTT Client initialisieren
mqtt_client = mqtt.Client(mqttClient.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect

# Auth setzen falls angegeben
if MQTT_USER and MQTT_PASSWORD:
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Verbindung aufbauen
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

@route('/weatherstation/updateweatherstation.php')
def receive_data():
    try:
        current_data.update({
            "zeitstempel": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
            "aussen_temperatur": f_to_c(request.query.tempf),
            "aussen_luftfeuchtigkeit": int(request.query.humidity),
            "aussen_taupunkt": f_to_c(request.query.dewptf),
            "luftdruck": min_to_hpa(request.query.baromin),
            "solarstrahlung": float(request.query.solarradiation),
            "uvindex": float(request.query.UV),
            "wind_geschwindigkeit_kmh": mph_to_kmh(request.query.windspeedmph),
            "wind_boeen_kmh": mph_to_kmh(request.query.windgustmph),
            "wind_richtung": deg_to_dir(request.query.winddir),
            "regen_live_mm": in_to_mm(request.query.rainin),
            "regen_heute_mm": in_to_mm(request.query.dailyrainin),
            "innen_temperatur": f_to_c(request.query.indoortempf),
            "innen_luftfeuchtigkeit": int(request.query.indoorhumidity),
        })

        # MQTT publish
        mqtt_payload = json.dumps(current_data)
        mqtt_client.publish(MQTT_TOPIC, mqtt_payload)
        print(f"[INFO] Gesendet an MQTT: {mqtt_payload}")

        return 'OK'

    except Exception as e:
        print(f"[ERROR] Fehler beim Verarbeiten der Anfrage: {e}")
        return 'Fehler', 500

@route('/data')
def show_data():
    response.content_type = 'application/json'
    return json.dumps(current_data)

run(host='0.0.0.0', port=8000)
