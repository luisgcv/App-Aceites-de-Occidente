import tkinter as tk
from tkinter import ttk, messagebox
from controllers import controlador_naturaleza_party
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

class VentanaNaturalezaPersona(tk.Frame):
    def __init__(self, parent):
        self.naturaleza_model = controlador_naturaleza_party

        self.id_seleccionado = None  

        super().__init__(parent, bg=COLOR_FONDO)
        
        # Configurar estilo para los widgets
        self._configurar_estilos()
        
        # Contenedor principal con sombra visual
        container = tk.Frame(self, bg=COLOR_FONDO)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Panel principal con borde sutil
        panel_principal = tk.Frame(container, bg=COLOR_PANEL, bd=2, 
                                 relief=tk.GROOVE, highlightbackground=COLOR_BORDE,
                                 highlightthickness=1)
        panel_principal.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Título con efecto de separación
        frame_titulo = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_titulo.pack(fill="x", pady=(10, 10), padx=20)

        titulo = tk.Label(frame_titulo, text="Gestión de Naturaleza de las Personas", 
                        font=FUENTE_TITULO, bg=COLOR_PANEL, 
                        fg=COLOR_PRIMARIO)
        titulo.pack(side="left")
     
        
        # Línea decorativa bajo el título
        tk.Frame(frame_titulo, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(5, 0))
        
        # Contenedor del formulario con fondo diferenciado
        frame_formulario = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_formulario.pack(fill="x", padx=20, pady=10)
        
        # Formulario con etiquetas y campos
        formulario = tk.Frame(frame_formulario, bg=COLOR_PANEL)
        formulario.pack(anchor="w", padx=10, pady=10)
        
        # Campo Nombre
        lbl_descripcion = tk.Label(formulario, text="Descripcion:", font=FUENTE_NORMAL, 
                            bg=COLOR_PANEL, fg=COLOR_TEXTO)
        lbl_descripcion.grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        
        self.entry_descripcion = tk.Entry(formulario, width=40, font=FUENTE_NORMAL,
                                   bg=COLOR_FONDO, fg=COLOR_TEXTO,
                                   insertbackground=COLOR_TEXTO,
                                   relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                   highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_descripcion.grid(row=0, column=1, pady=8)
        


        # Contenedor para la tabla con scroll
        frame_tabla = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        # Tabla de personas con estilo personalizado
        columnas = ("id", "descripcion")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                 yscrollcommand=scrollbar.set)
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), anchor="w")
            self.tabla.column(col, width=150, anchor="w")
        
        self.tabla.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla.yview)
        
        self.cargar_naturaleza()

        # Contenedor invisible para los botones
        boton_frame = tk.Frame(panel_principal, bg=COLOR_PANEL)
        boton_frame.pack(pady=(5, 15))

        # Botón Guardar
        btn_guardar = tk.Button(boton_frame, text="Guardar Naturaleza", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.guardar_naturaleza)
        btn_guardar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_guardar.bind("<Enter>", lambda e: btn_guardar.config(bg=COLOR_HOVER))
        btn_guardar.bind("<Leave>", lambda e: btn_guardar.config(bg=COLOR_PRIMARIO))

        # Botón Eliminar
        btn_eliminar = tk.Button(boton_frame, text="Eliminar Naturaleza", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.eliminar_naturaleza)
        btn_eliminar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_eliminar.bind("<Enter>", lambda e: btn_eliminar.config(bg=COLOR_HOVER))
        btn_eliminar.bind("<Leave>", lambda e: btn_eliminar.config(bg=COLOR_PRIMARIO))

        # Botón actualizar
        btn_actualizar= tk.Button(boton_frame, text="Actualizar Naturaleza", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.actualizar_naturaleza)
        btn_actualizar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg=COLOR_HOVER))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg=COLOR_PRIMARIO))


        # Botón Limpiar
        btn_limpiar= tk.Button(boton_frame, text="Limpiar", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.limpiar)
        btn_limpiar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_limpiar.bind("<Enter>", lambda e: btn_limpiar.config(bg=COLOR_HOVER))
        btn_limpiar.bind("<Leave>", lambda e: btn_limpiar.config(bg=COLOR_PRIMARIO))


        ## 
        def al_seleccionar(event):
            item = self.tabla.focus()
            if item:

                valores = self.tabla.item(item, "values")
                self.id_seleccionado = None
                self.id_seleccionado = int(valores[0])
                self.entry_descripcion.delete(0, tk.END)
                self.entry_descripcion.insert(0, valores[1])
                

        self.tabla.bind("<<TreeviewSelect>>", al_seleccionar)
    


    def _configurar_estilos(self):
        """Configura los estilos para los widgets ttk"""
        estilo = ttk.Style()
        
        # Configurar estilo para Treeview
        estilo.configure("Treeview", 
                        background=COLOR_FONDO,
                        foreground=COLOR_TEXTO,
                        fieldbackground=COLOR_FONDO,
                        borderwidth=0,
                        font=FUENTE_NORMAL)
        
        estilo.configure("Treeview.Heading", 
                        background=COLOR_BORDE,
                        foreground=COLOR_TEXTO,
                        font=FUENTE_BOTON,
                        relief="flat")
        
        estilo.map("Treeview", 
                  background=[("selected", COLOR_PRIMARIO_OSCURO)],
                  foreground=[("selected", COLOR_TEXTO)])
        
        # Estilo para separadores
        estilo.configure("TSeparator", background=COLOR_BORDE)

    def limpiar(self):
        self.cargar_naturaleza()
        self.id_seleccionado = None 
        self.entry_descripcion.delete(0, tk.END)

    def cargar_naturaleza(self):
        """Carga las personas en la tabla"""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        datos = self.naturaleza_model.mostrar_naturaleza()
        if datos: 
            if isinstance(datos, list):
                for naturaleza in datos:
                    self.tabla.insert('', 'end', values=naturaleza)
            else:
                mensajes.mensajes_Error(f"No se pudieron cargar las naturalezas:\n{datos}")
   


    def eliminar_naturaleza(self): 
        self.naturaleza_model.eliminar_naturaleza(self.id_seleccionado)
        self.limpiar()


    def actualizar_naturaleza(self): 
        self.naturaleza_model.actualizar_naturaleza(self.id_seleccionado,self.entry_descripcion.get())

        self.limpiar()


    def guardar_naturaleza(self):
        self.naturaleza_model.guardar_naturaleza(self.entry_descripcion.get())
        self.limpiar()
