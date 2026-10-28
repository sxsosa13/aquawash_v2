import csv
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox, filedialog

from config import MONEDA
from database import db
from ui.utils import tabla, llenar


class ReportesTab(ttk.Frame):
    """Ingresos por día, servicios más solicitados y exportación a CSV (solo ADMIN)."""

    def __init__(self, master):
        super().__init__(master, padding=10)
        hoy = date.today()
        self.desde = tk.StringVar(value=hoy.replace(day=1).isoformat())
        self.hasta = tk.StringVar(value=hoy.isoformat())
        self.ingresos = []

        f = ttk.Frame(self)
        f.pack(fill="x")
        ttk.Label(f, text="Desde").pack(side="left")
        ttk.Entry(f, textvariable=self.desde, width=12).pack(side="left", padx=4)
        ttk.Label(f, text="Hasta").pack(side="left")
        ttk.Entry(f, textvariable=self.hasta, width=12).pack(side="left", padx=4)
        ttk.Button(f, text="Generar", command=self.generar).pack(side="left", padx=6)
        ttk.Button(f, text="Exportar CSV", command=self.exportar).pack(side="left")
        self.lbl = ttk.Label(f, text="", font=("Segoe UI", 11, "bold"))
        self.lbl.pack(side="right")

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True, pady=10)
        izq = ttk.LabelFrame(cuerpo, text="Ingresos por día", padding=6)
        izq.pack(side="left", fill="both", expand=True)
        marco, self.tv = tabla(izq, [("dia", "Día", 120), ("total", f"Total ({MONEDA})", 130)], alto=14)
        marco.pack(fill="both", expand=True)
        der = ttk.LabelFrame(cuerpo, text="Servicios más solicitados", padding=6)
        der.pack(side="left", fill="both", expand=True, padx=(10, 0))
        self.canvas = tk.Canvas(der, width=380, height=300, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.generar()

    def generar(self):
        try:
            d, h = date.fromisoformat(self.desde.get()), date.fromisoformat(self.hasta.get())
        except ValueError:
            return messagebox.showwarning("Fechas inválidas", "Use el formato AAAA-MM-DD.")
        self.ingresos = db.ingresos_por_dia(d, h)
        llenar(self.tv, [(i, (r["dia"].isoformat(), f"{r['total']:,.2f}")) for i, r in enumerate(self.ingresos)])
        total = sum(r["total"] for r in self.ingresos)
        self.lbl.config(text=f"Total del período: {MONEDA}{total:,.2f}")
        self.graficar(db.servicios_top(d, h))

    def graficar(self, datos):
        c = self.canvas
        c.delete("all")
        if not datos:
            c.create_text(190, 120, text="Sin datos en el período", fill="#777")
            return
        maximo = max(r["cantidad"] for r in datos)
        for i, r in enumerate(datos[:8]):
            y = 14 + i * 34
            c.create_text(4, y + 11, anchor="w", text=r["nombre"][:24], font=("Segoe UI", 9))
            ancho = int(150 * r["cantidad"] / maximo)
            c.create_rectangle(190, y, 190 + ancho, y + 22, fill="#2a9d8f", outline="")
            c.create_text(196 + ancho, y + 11, anchor="w", text=str(r["cantidad"]), font=("Segoe UI", 9, "bold"))

    def exportar(self):
        if not self.ingresos:
            return messagebox.showinfo("Sin datos", "Genere primero un reporte con datos.")
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")],
                                            initialfile="ingresos.csv")
        if ruta:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["dia", "total"])
                w.writerows([[r["dia"].isoformat(), r["total"]] for r in self.ingresos])
            messagebox.showinfo("Exportado", f"Archivo guardado en:\n{ruta}")
