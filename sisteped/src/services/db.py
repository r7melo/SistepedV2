import mysql.connector
import json
import os
from pathlib import Path

try:
    CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
except Exception:
    config = {}

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", config.get("DB_HOST")),
    "user": os.environ.get("DB_USER", config.get("DB_USER")),
    "password": os.environ.get("DB_PASSWORD", config.get("DB_PASSWORD")),
    "database": os.environ.get("DB_NAME", config.get("DB_NAME")),
}

port_val = os.environ.get("DB_PORT", config.get("DB_PORT"))
if port_val:
    DB_CONFIG["port"] = int(port_val)

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        host_alvo = DB_CONFIG.get('host', 'Não definido')
        print(f"Erro de conexão ({host_alvo}): {err}")
        return None
