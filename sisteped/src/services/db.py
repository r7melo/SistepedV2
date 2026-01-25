import mysql.connector
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

DB_CONFIG = {
    "host": config.get("DB_HOST"),
    "user": config.get("DB_USER"),
    "password": config.get("DB_PASSWORD"),
    "database": config.get("DB_NAME"),
    "port": config.get("DB_PORT")
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None