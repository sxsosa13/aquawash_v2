"""Servidor web de Sosa Car Wash: sirve la página principal y una API JSON básica."""
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import WEB_PORT
from database import db

RAIZ = os.path.dirname(os.path.abspath(__file__))


class Handler(BaseHTTPRequestHandler):
    def _responder(self, cuerpo, tipo, codigo=200):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _json(self, datos, codigo=200):
        self._responder(json.dumps(datos, default=str).encode(), "application/json; charset=utf-8", codigo)

    def do_GET(self):
        url = urlparse(self.path)
        try:
            if url.path in ("/", "/index.html"):
                with open(os.path.join(RAIZ, "index.html"), "rb") as f:
                    self._responder(f.read(), "text/html; charset=utf-8")
            elif url.path == "/api/servicios":
                self._json(db.consultar("SELECT id, nombre, tipo_vehiculo, precio, duracion_min FROM servicios WHERE activo ORDER BY tipo_vehiculo, precio"))
            elif url.path == "/api/horarios":
                self._json(db.horarios_disponibles(parse_qs(url.query).get("fecha", [""])[0]))
            elif url.path == "/api/insumos":
                self._json(db.listar_insumos())
            elif url.path == "/api/balance":
                qs = parse_qs(url.query)
                desde = qs.get("desde", [str(db.consultar("SELECT MIN(fecha) FROM ingresos")[0]["min"]) or "2024-01-01"])[0]
                hasta = qs.get("hasta", [str(db.consultar("SELECT MAX(fecha) FROM ingresos")[0]["max"]) or "2100-12-31"])[0]
                self._json(db.balance_economico(desde, hasta))
            else:
                self.send_error(404)
        except ValueError:
            self._json({"error": "Fecha inválida"}, 400)
        except Exception:
            self._json({"error": "Error interno del servidor"}, 500)

    def do_POST(self):
        if self.path == "/api/reservas":
            try:
                largo = int(self.headers.get("Content-Length", 0))
                cita = db.reserva_web(json.loads(self.rfile.read(largo)))
                self._json({"ok": True, "cita": cita}, 201)
            except ValueError as e:
                self._json({"ok": False, "error": str(e) or "Datos inválidos"}, 400)
            except Exception:
                self._json({"ok": False, "error": "Error interno del servidor"}, 500)
        elif self.path == "/api/contacto":
            try:
                largo = int(self.headers.get("Content-Length", 0))
                datos = json.loads(self.rfile.read(largo))
                db.registrar_contacto(datos.get("nombre", ""), datos.get("telefono", ""), datos.get("email", ""), datos.get("mensaje", ""))
                self._json({"ok": True, "mensaje": "Gracias por contactarnos."}, 201)
            except Exception:
                self._json({"ok": False, "error": "No se pudo enviar el mensaje"}, 500)
        else:
            self.send_error(404)

    def log_message(self, *args):
        pass


def iniciar_en_hilo():
    srv = ThreadingHTTPServer(("0.0.0.0", WEB_PORT), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


if __name__ == "__main__":
    print(f"Sosa Car Wash web en http://localhost:{WEB_PORT}  (Ctrl+C para detener)")
    ThreadingHTTPServer(("0.0.0.0", WEB_PORT), Handler).serve_forever()
