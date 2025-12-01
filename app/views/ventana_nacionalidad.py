import tkinter as tk
from tkinter import ttk, messagebox
from controllers import controlador_nacionalidad
from utils.mensajes import mensajes

# Paleta de colores actualizada
COLOR_FONDO = "#1B1F2A"          # Fondo principal (oscuro)
COLOR_PANEL = "#252B3A"          # Paneles y marcos
COLOR_TEXTO = "#FFFFFF"          # Texto principal (blanco puro)
COLOR_TEXTO_SEC = "#B0B4C8"      # Texto secundario (más claro)
COLOR_PRIMARIO = "#2ECC71"       # Verde moderno (principal)
COLOR_PRIMARIO_OSCURO = "#27AE60" # Verde oscuro (hover)
COLOR_HOVER = "#34D178"          # Verde hover (más suave)
COLOR_ACCION = "#4CAF50"         # Verde acción (para confirmaciones)
COLOR_BORDE = "#34495E"          # Color para bordes sutiles

# Fuentes actualizadas
FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 14)
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")
FUENTE_MENU = ("Segoe UI", 11)


class VentanaNacionalidad(tk.Frame):
    def __init__(self, parent):
        self.nacionalidad_model = controlador_nacionalidad
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

        titulo = tk.Label(frame_titulo, text="Gestión de Nacionalidades", 
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

        self.cargar_nacionalidades()

        boton_frame = tk.Frame(panel_principal, bg=COLOR_PANEL)
        boton_frame.pack(pady=(5, 15))

        self._crear_boton(boton_frame, "Guardar Nacionalidad", self.guardar_nacionalidad)
        self._crear_boton(boton_frame, "Eliminar Nacionalidad", self.eliminar_nacionalidad)
        self._crear_boton(boton_frame, "Actualizar Nacionalidad", self.actualizar_nacionalidad)
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
        self.cargar_nacionalidades()
        self.id_seleccionado = None
        self.entry_descripcion.delete(0, tk.END)

    def cargar_nacionalidades(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        datos = self.nacionalidad_model.mostrar_nacionalidad()
        if datos:
            if isinstance(datos, list):
                for nac in datos:
                    self.tabla.insert('', 'end', values=nac)
            else:
                mensajes.mensajes_Error(f"No se pudieron cargar las nacionalidades:\n{datos}")

    def guardar_nacionalidad(self):
        self.nacionalidad_model.guardar_nacionalidad(self.entry_descripcion.get())
        self.limpiar()

    def eliminar_nacionalidad(self):
        self.nacionalidad_model.eliminar_nacionalidad(self.id_seleccionado)
        self.limpiar()

    def actualizar_nacionalidad(self):
        self.nacionalidad_model.actualizar_nacionalidad(self.id_seleccionado, self.entry_descripcion.get())
        self.limpiar()

    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = int(valores[0])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[1])
