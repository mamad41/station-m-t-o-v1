import sqlite3

DB_NAME = "measures.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sensor_id TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            raw_payload TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_measure(sensor_id, temperature, humidity, wind_speed, raw_payload):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (sensor_id, temperature, humidity, wind_speed, raw_payload)
        VALUES (?, ?, ?, ?, ?)
    """, (sensor_id, temperature, humidity, wind_speed, raw_payload))
    conn.commit()
    conn.close()