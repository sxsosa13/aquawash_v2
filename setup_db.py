"""Crea la base de datos, las tablas y los datos iniciales.
    python setup_db.py          -> estructura + usuarios y servicios iniciales
    python setup_db.py --demo   -> además carga clientes y citas de ejemplo
"""
import os
import sys

from database import db

db.inicializar()
print("✔ Base de datos lista (tablas, usuarios y servicios iniciales).")

if "--demo" in sys.argv:
    if db.consultar("SELECT 1 FROM clientes LIMIT 1"):
        print("• Ya existen clientes; no se cargaron datos de ejemplo.")
    else:
        with open(os.path.join("sql", "datos_demo.sql"), encoding="utf-8") as f:
            db.ejecutar(f.read())
        print("✔ Datos de ejemplo cargados.")
