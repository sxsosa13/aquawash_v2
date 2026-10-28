import tkinter as tk
from tkinter import ttk, messagebox

from database import db


class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AquaWash · Ingreso")
        self.resizable(False, False)
        self.usuario = None
        self.u, self.p = tk.StringVar(), tk.StringVar()

        f = ttk.Frame(self, padding=28)
        f.pack()
        ttk.Label(f, text="AquaWash", font=("Segoe UI", 22, "bold")).grid(columnspan=2)
        ttk.Label(f, text="Lavadero de autos y motos").grid(columnspan=2, pady=(0, 14))
        ttk.Label(f, text="Usuario").grid(row=2, column=0, sticky="e", pady=4)
        entrada = ttk.Entry(f, textvariable=self.u, width=24)
        entrada.grid(row=2, column=1, padx=6)
        ttk.Label(f, text="Contraseña").grid(row=3, column=0, sticky="e", pady=4)
        ttk.Entry(f, textvariable=self.p, show="•", width=24).grid(row=3, column=1, padx=6)
        ttk.Button(f, text="Ingresar", command=self.ingresar).grid(row=4, columnspan=2, pady=14)
        self.bind("<Return>", lambda _e: self.ingresar())
        entrada.focus()

    def ingresar(self):
        try:
            usuario = db.autenticar(self.u.get().strip(), self.p.get())
        except Exception as e:
            return messagebox.showerror("Error de conexión", f"No se pudo consultar la base de datos:\n{db.mensaje_error(e)}")
        if usuario:
            self.usuario = usuario
            self.destroy()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
