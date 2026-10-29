"""Configuración central de Sosa Car Wash.
La conexión a PostgreSQL se guarda en config_local.json (lo crea el asistente configurar_bd.py).
También puede definirse con variables de entorno AQUAWASH_DB_*."""
import json
import os

_AQUI = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG = {
    "host": os.getenv("AQUAWASH_DB_HOST", "localhost"),
    "port": int(os.getenv("AQUAWASH_DB_PORT", "5432")),
    "dbname": os.getenv("AQUAWASH_DB_NAME", "aquawash"),
    "user": os.getenv("AQUAWASH_DB_USER", "postgres"),
    "password": os.getenv("AQUAWASH_DB_PASSWORD", ""),
}

_local = os.path.join(_AQUI, "config_local.json")
if os.path.exists(_local):
    with open(_local, encoding="utf-8") as _f:
        DB_CONFIG.update(json.load(_f))

PUESTOS_SIMULTANEOS = 2
HORARIOS = [f"{h:02d}:00" for h in range(8, 18)]
MONEDA = "₲"
SITE_NAME = "Sosa Car Wash"
WEB_PORT = 8000
