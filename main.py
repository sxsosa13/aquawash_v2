"""AquaWash · Sistema de gestión para lavadero de autos y motos.
Ejecutar:  python main.py
"""
import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox

from config import WEB_PORT
from database import db
from ui.citas import CitasTab
from ui.clientes import ClientesTab
from ui.login import Login
from ui.reportes import ReportesTab
from ui.servicios import ServiciosTab
from web import server


class App(tk.Tk):
    def __init__(self, usuario):
        super().__init__()
        self.title("AquaWash · Gestión de lavadero")
        self.geometry("1100x720")
        self.minsize(980, 640)
        self.servidor = None

        menu = tk.Menu(self)
        archivo = tk.Menu(menu, tearoff=0)
        archivo.add_command(label="Iniciar servidor web", command=self.iniciar_web)
        archivo.add_command(label="Abrir página web", command=self.abrir_web)
        archivo.add_separator()
        archivo.add_command(label="Salir", command=self.destroy)
        menu.add_cascade(label="Archivo", menu=archivo)
        self.config(menu=menu)

        cab = ttk.Frame(self, padding=(12, 8))
        cab.pack(fill="x")
        ttk.Label(cab, text="AquaWash", font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Label(cab, text=f"{usuario['nombre']} · {usuario['rol']}").pack(side="right")

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.citas, self.clientes = CitasTab(self.nb), ClientesTab(self.nb)
        self.nb.add(self.citas, text="  Agenda  ")
        self.nb.add(self.clientes, text="  Clientes y vehículos  ")
        if usuario["rol"] == "ADMIN":
            self.nb.add(ServiciosTab(self.nb), text="  Servicios  ")
            self.nb.add(ReportesTab(self.nb), text="  Reportes  ")
        self.nb.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

    def al_cambiar_pestana(self, _e=None):
        if self.nb.select() == str(self.citas):   # refresca datos (incluye reservas web nuevas)
            self.citas.refrescar_combos()
            self.citas.cargar()

    def iniciar_web(self):
        if self.servidor:
            return messagebox.showinfo("Servidor web", f"Ya está activo en http://localhost:{WEB_PORT}")
        try:
            self.servidor = server.iniciar_en_hilo()
        except OSError as e:
            return messagebox.showerror("Servidor web", f"No se pudo iniciar (¿puerto ocupado?):\n{e}")
        messagebox.showinfo("Servidor web", f"Página activa en http://localhost:{WEB_PORT}")

    def abrir_web(self):
        self.iniciar_web() if not self.servidor else None
        webbrowser.open(f"http://localhost:{WEB_PORT}")


def main():
    try:
        db.inicializar()
    except Exception as e:
        raiz = tk.Tk()
        raiz.withdraw()
        messagebox.showerror("Base de datos", f"No se pudo conectar a PostgreSQL:\n\n{db.mensaje_error(e)}\n\n"
                                              "Revise en config.py la contraseña, el puerto y el usuario, "
                                              "y que el servicio de PostgreSQL esté iniciado.")
        return
    login = Login()
    login.mainloop()
    if login.usuario:
        App(login.usuario).mainloop()


if __name__ == "__main__":
    main()
