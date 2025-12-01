import tkinter as tk   
from tkinter import ttk
from controllers import controlador_puesto
from utils.mensajes import mensajes

# Paleta de colores
COLOR_FONDO = "#1B1F2A"
COLOR_PANEL = "#252B3A"
COLOR_TEXTO = "#FFFFFF"
COLOR_PRIMARIO = "#2ECC71"
COLOR_PRIMARIO_OSCURO = "#27AE60"
COLOR_HOVER = "#34D178"
COLOR_BORDE = "#34495E"

# Fuentes
FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")


class VentanaPuestoTrabajo(tk.Frame):
    def __init__(self, parent):
        self.puesto_model = controlador_puesto
        self.id_seleccionado = None  
        
        super().__init__(parent, bg=COLOR_FONDO)
        
        self._configurar_estilos()
        
        container = tk.Frame(self, bg=COLOR_FONDO)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        panel_principal = tk.Frame(container, bg=COLOR_PANEL, bd=2, relief=tk.GROOVE,
                                   highlightbackground=COLOR_BORDE, highlightthickness=1)
        panel_principal.pack(fill="both", expand=True, padx=5, pady=5)
        
        frame_titulo = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_titulo.pack(fill="x", pady=(10, 10), padx=20)

        titulo = tk.Label(frame_titulo, text="Gestión de Puestos de Trabajo", 
                          font=FUENTE_TITULO, bg=COLOR_PANEL, fg=COLOR_PRIMARIO)
        titulo.pack(side="left")
        
        tk.Frame(frame_titulo, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(5, 0))
        
        frame_formulario = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_formulario.pack(fill="x", padx=20, pady=10)

        formulario = tk.Frame(frame_formulario, bg=COLOR_PANEL)
        formulario.pack(anchor="w", padx=10, pady=10)
        
        lbl_descripcion = tk.Label(formulario, text="Descripción:", font=FUENTE_NORMAL, 
                                   bg=COLOR_PANEL, fg=COLOR_TEXTO)
        lbl_descripcion.grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))

        self.entry_descripcion = tk.Entry(formulario, width=40, font=FUENTE_NORMAL,
                                          bg=COLOR_FONDO, fg=COLOR_TEXTO,
                                          insertbackground=COLOR_TEXTO,
                                          relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                          highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_descripcion.grid(row=0, column=1, pady=8)

        frame_tabla = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = ("id", "descripcion")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                  yscrollcommand=scrollbar.set)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), anchor="w")
            self.tabla.column(col, width=150, anchor="w")

        self.tabla.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla.yview)

        self.cargar_puestos()

        boton_frame = tk.Frame(panel_principal, bg=COLOR_PANEL)
        boton_frame.pack(pady=(5, 15))

        self._crear_boton(boton_frame, "Guardar Puesto", self.guardar_puesto)
        self._crear_boton(boton_frame, "Eliminar Puesto", self.eliminar_puesto)
        self._crear_boton(boton_frame, "Actualizar Puesto", self.actualizar_puesto)
        self._crear_boton(boton_frame, "Limpiar", self.limpiar)

        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

    def _crear_boton(self, frame, texto, comando):
        boton = tk.Button(frame, text=texto, bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                          font=FUENTE_BOTON, relief=tk.FLAT,
                          activebackground=COLOR_PRIMARIO_OSCURO,
                          activeforeground=COLOR_TEXTO, command=comando)
        boton.pack(side="left", padx=10, ipadx=15, ipady=5)
        boton.bind("<Enter>", lambda e: boton.config(bg=COLOR_HOVER))
        boton.bind("<Leave>", lambda e: boton.config(bg=COLOR_PRIMARIO))

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, borderwidth=0, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", background=COLOR_BORDE,
                         foreground=COLOR_TEXTO, font=FUENTE_BOTON, relief="flat")
        estilo.map("Treeview", background=[("selected", COLOR_PRIMARIO_OSCURO)],
                   foreground=[("selected", COLOR_TEXTO)])
        estilo.configure("TSeparator", background=COLOR_BORDE)

    def limpiar(self):
        self.cargar_puestos()
        self.id_seleccionado = None
        self.entry_descripcion.delete(0, tk.END)

    def cargar_puestos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        datos = self.puesto_model.mostrar_puestos()
        if datos:
            if isinstance(datos, list):
                for puesto in datos:
                    self.tabla.insert('', 'end', values=puesto)
            else:
                mensajes.mensajes_Error(f"No se pudieron cargar los puestos:\n{datos}")

    def guardar_puesto(self):
        self.puesto_model.guardar_puesto(self.entry_descripcion.get())
        self.limpiar()

    def eliminar_puesto(self):
        self.puesto_model.eliminar_puesto(self.id_seleccionado)
        self.limpiar()

    def actualizar_puesto(self):
        self.puesto_model.actualizar_puesto(self.id_seleccionado, self.entry_descripcion.get())
        self.limpiar()

    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = int(valores[0])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[1])
