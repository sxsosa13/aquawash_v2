"""Utilidades de interfaz reutilizables."""
from tkinter import ttk


def tabla(parent, columnas, alto=10):
    """Crea un Treeview con scroll. columnas = [(clave, titulo, ancho), ...]. Devuelve (marco, tree)."""
    marco = ttk.Frame(parent)
    tv = ttk.Treeview(marco, columns=[c[0] for c in columnas], show="headings",
                      height=alto, selectmode="browse")
    for clave, titulo, ancho in columnas:
        tv.heading(clave, text=titulo)
        tv.column(clave, width=ancho, anchor="w")
    sb = ttk.Scrollbar(marco, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=sb.set)
    tv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return marco, tv


def llenar(tv, filas):
    """filas = [(id, (valores...)), ...]"""
    tv.delete(*tv.get_children())
    for iid, valores in filas:
        tv.insert("", "end", iid=str(iid), values=valores)


def seleccionado(tv):
    sel = tv.selection()
    return int(sel[0]) if sel else None
