from bottle import request, route, run
import datetime, json
import paho.mqtt.client as mqtt
import bashio

# MQTT Konfiguration aus Add-on Optionen lesen
MQTT_HOST = bashio.config('mqtt_host')
MQTT_PORT = bashio.config('mqtt_port')
MQTT_USER = bashio.config('mqtt_username')
MQTT_PASS = bashio.config('mqtt_password')
MQTT_TOPIC_PREFIX = bashio.config('mqtt_topic_prefix')

current_data = {}

WIND_DIRS = [
    'N', 'NNE', 'NE', 'ENE',
    'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW',
    'W', 'WNW', 'NW', 'NNW'
]

def deg_to_dir(deg):
    return WIND_DIRS[round(int(deg)/22.5) % 16]

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

# MQTT Client einrichten
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

@route('/weatherstation/updateweatherstation.php')
def receive_data():
    try:
        current_data.update({
            "timestamp": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
            "pressure_hpa": min_to_hpa(request.query.baromin),
            "temperature_c": f_to_c(request.query.tempf),
            "humidity": int(request.query.humidity),
            "wind_speed_kmh": mph_to_kmh(request.query.windspeedmph),
            "wind_direction_compass": deg_to_dir(request.query.winddir),
            "rain_mm": in_to_mm(request.query.rainin),
            "solar_radiation": float(request.query.solarradiation),
            "uv": float(request.query.UV),
        })

        # Daten einzeln als MQTT Topics publishen
        for key, value in current_data.items():
            topic = f"{MQTT_TOPIC_PREFIX}/{key}"
            mqtt_client.publish(topic, str(value), retain=True)

        return 'OK'
    except Exception as e:
        return str(e)

@route('/data')
def show_data():
    return json.dumps(current_data)

run(host='0.0.0.0', port=8000)
