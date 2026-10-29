import tkinter as tk
from tkinter import ttk, messagebox

from config import MONEDA
from database import db
from ui.utils import tabla, llenar, seleccionado


class ServiciosTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.sid = None
        self.v = {"nombre": tk.StringVar(), "tipo": tk.StringVar(value="AUTO"),
                  "precio": tk.StringVar(), "duracion": tk.StringVar(value="60")}
        f = ttk.LabelFrame(self, text="Servicio", padding=8)
        f.pack(fill="x")
        campos = [("Nombre", "nombre", 28), ("Precio", "precio", 10), ("Minutos", "duracion", 6)]
        ttk.Label(f, text="Vehículo").pack(side="left")
        ttk.Combobox(f, textvariable=self.v["tipo"], values=["AUTO", "MOTO"], width=7,
                     state="readonly").pack(side="left", padx=4)
        for txt, k, w in campos:
            ttk.Label(f, text=txt).pack(side="left", padx=(8, 0))
            ttk.Entry(f, textvariable=self.v[k], width=w).pack(side="left", padx=4)
        ttk.Button(f, text="Guardar", command=self.guardar).pack(side="left", padx=4)
        ttk.Button(f, text="Nuevo", command=self.nuevo).pack(side="left")
        ttk.Button(f, text="Activar / desactivar", command=self.alternar).pack(side="left", padx=4)

        marco, self.tv = tabla(self, [("nombre", "Servicio", 280), ("tipo", "Vehículo", 90),
                                      ("precio", f"Precio ({MONEDA})", 110), ("min", "Minutos", 80),
                                      ("activo", "Activo", 80)], alto=14)
        marco.pack(fill="both", expand=True, pady=8)
        self.tv.bind("<<TreeviewSelect>>", self.al_seleccionar)
        self.cargar()

    def cargar(self):
        filas = db.consultar("SELECT * FROM servicios ORDER BY tipo_vehiculo, precio")
        llenar(self.tv, [(r["id"], (r["nombre"], r["tipo_vehiculo"], f"{r['precio']:,.0f}",
                                     r["duracion_min"], "Sí" if r["activo"] else "No")) for r in filas])

    def nuevo(self):
        self.sid = None
        self.v["nombre"].set("")
        self.v["precio"].set("")
        self.v["duracion"].set("60")
        self.tv.selection_remove(self.tv.selection())

    def al_seleccionar(self, _e=None):
        sid = seleccionado(self.tv)
        if sid is None:
            return
        self.sid = sid
        r = db.consultar("SELECT * FROM servicios WHERE id = %s", (sid,))[0]
        self.v["nombre"].set(r["nombre"])
        self.v["tipo"].set(r["tipo_vehiculo"])
        self.v["precio"].set(str(r["precio"]))
        self.v["duracion"].set(str(r["duracion_min"]))

    def guardar(self):
        try:
            nombre = self.v["nombre"].get().strip()
            precio = float(self.v["precio"].get().replace(",", "."))
            minutos = int(self.v["duracion"].get())
            if not nombre or precio < 0 or minutos <= 0:
                raise ValueError
        except ValueError:
            return messagebox.showwarning("Datos inválidos", "Revise nombre, precio (número) y minutos (entero).")
        datos = (nombre, self.v["tipo"].get(), precio, minutos)
        if self.sid:
            db.ejecutar("UPDATE servicios SET nombre=%s, tipo_vehiculo=%s, precio=%s, duracion_min=%s WHERE id=%s", datos + (self.sid,))
        else:
            db.ejecutar("INSERT INTO servicios (nombre, tipo_vehiculo, precio, duracion_min) VALUES (%s, %s, %s, %s)", datos)
        self.nuevo()
        self.cargar()

    def alternar(self):
        if self.sid:
            db.ejecutar("UPDATE servicios SET activo = NOT activo WHERE id = %s", (self.sid,))
            self.cargar()
