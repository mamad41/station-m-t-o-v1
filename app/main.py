from fastapi import FastAPI
from dotenv import load_dotenv
import sqlite3

load_dotenv()

from app.database import init_db
from app.mqtt_client import start_mqtt

init_db()
start_mqtt()

app = FastAPI(title="CCI IoT - SenseCAP Tracker")

@app.get("/measures")
def get_measures(limit: int = 50):
    conn = sqlite3.connect("measures.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "timestamp": r[1], "sensor_id": r[2], "temperature": r[3], "humidity": r[4], "wind_speed": r[5]} for r in rows]