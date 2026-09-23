import json
import os
import paho.mqtt.client as mqtt
from app.database import save_measure
from app.notifier import send_alert_email

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connecté avec le code retour {rc}")
    topic = os.getenv("MQTT_TOPIC")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)
        
        # Adaptation selon le format du payload SenseCAP reçu
        sensor_id = data.get("device_id", msg.topic.split("/")[-1])
        temp = data.get("temperature")
        humidity = data.get("humidity")
        wind_speed = data.get("wind_speed")

        # Sauvegarde en BDD
        save_measure(sensor_id, temp, humidity, wind_speed, payload_str)

        # Vérification des seuils
        temp_max = float(os.getenv("TEMP_MAX_THRESHOLD", 40))
        if temp is not None and temp > temp_max:
            send_alert_email(
                subject=f"Alerte Température - Capteur {sensor_id}",
                message=f"Température critique détectée : {temp}°C (seuil : {temp_max}°C)"
            )
            
    except Exception as e:
        print(f"[MQTT] Erreur de traitement : {e}")

def start_mqtt():
    client = mqtt.Client()
    user = os.getenv("MQTT_USER")
    pwd = os.getenv("MQTT_PASSWORD")
    if user and pwd:
        client.username_pw_set(user, pwd)

    client.on_connect = on_connect
    client.on_message = on_message

    broker = os.getenv("MQTT_BROKER")
    port = int(os.getenv("MQTT_PORT", 1883))
    client.connect(broker, port, 60)
    client.loop_start()