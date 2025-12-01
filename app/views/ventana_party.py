import tkinter as tk
from tkinter import ttk, messagebox
from controllers import controlador_party,controlador_naturaleza_party,controlador_cliente
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

class VentanaParty(tk.Frame):
    def __init__(self, parent):
        self.es_cliente_var = tk.StringVar(value="No")

        self.party_model = controlador_party

        self.id_seleccionado = None  

        super().__init__(parent, bg=COLOR_FONDO)
        
        # Configurar estilo para los widgets
        self._configurar_estilos()
        
  # Scrollable Container
        canvas = tk.Canvas(self, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_FONDO)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def resize_scrollable_frame(event):
            canvas.itemconfig(window, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        panel = tk.Frame(scrollable_frame, bg=COLOR_PANEL, bd=2, relief=tk.GROOVE)
        panel.pack(fill="both", expand=True)

        
        # Título con efecto de separación
        frame_titulo = tk.Frame(panel, bg=COLOR_PANEL)
        frame_titulo.pack(fill="x", pady=(10, 10), padx=20)




        titulo = tk.Label(frame_titulo, text="Gestión de Personas", 
                        font=FUENTE_TITULO, bg=COLOR_PANEL, 
                        fg=COLOR_PRIMARIO)
        titulo.pack(side="left")
     
        
        # Línea decorativa bajo el título
        tk.Frame(frame_titulo, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(5, 0))
        
        # Contenedor del formulario con fondo diferenciado
        frame_formulario = tk.Frame(panel, bg=COLOR_PANEL)
        frame_formulario.pack(fill="x", padx=20, pady=10)
        
        # Formulario con etiquetas y campos
        formulario = tk.Frame(frame_formulario, bg=COLOR_PANEL)
        formulario.pack(anchor="w", padx=10, pady=10)

        cliente_frame = tk.Frame(formulario, bg=COLOR_FONDO)
        cliente_frame.grid(row=6, column=0, columnspan=2, pady=(10, 5), sticky="w")

        tk.Label(cliente_frame, text="¿Es cliente?", fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(side="left")

        rb_si = tk.Radiobutton(cliente_frame, text="Sí", variable=self.es_cliente_var, value="Sí",
                            bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor=COLOR_PANEL,
                            activebackground=COLOR_HOVER)
        rb_si.pack(side="left", padx=(10, 5))

        rb_no = tk.Radiobutton(cliente_frame, text="No", variable=self.es_cliente_var, value="No",
                            bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor=COLOR_PANEL,
                            activebackground=COLOR_HOVER)
        rb_no.pack(side="left", padx=(10, 5))

        
        # Campo Nombre
        lbl_nombre = tk.Label(formulario, text="Nombre:", font=FUENTE_NORMAL, 
                            bg=COLOR_PANEL, fg=COLOR_TEXTO)
        lbl_nombre.grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        
        self.entry_nombre = tk.Entry(formulario, width=40, font=FUENTE_NORMAL,
                                   bg=COLOR_FONDO, fg=COLOR_TEXTO,
                                   insertbackground=COLOR_TEXTO,
                                   relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                   highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_nombre.grid(row=0, column=1, pady=8)
        
        # Campo Naturaleza
        lbl_naturaleza = tk.Label(formulario, text="Naturaleza:", font=FUENTE_NORMAL,
                                bg=COLOR_PANEL, fg=COLOR_TEXTO)
        lbl_naturaleza.grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))

        estilo_combo = ttk.Style()
        estilo_combo.configure("TCombobox", fieldbackground=COLOR_FONDO,
                            background=COLOR_FONDO, foreground=COLOR_BORDE,
                            selectbackground=COLOR_PRIMARIO_OSCURO,
                            selectforeground=COLOR_TEXTO)

        # Obtener las naturalezas disponibles
        resultado = controlador_naturaleza_party.mostrar_naturaleza()

        if not resultado or isinstance(resultado, str):
            # No hay naturalezas
            nombres = []
            mensajes.mensajes_Error("No hay naturaleza registrada. Agregue una antes de continuar.")

            # Crear combobox vacío
            self.combo_naturaleza = ttk.Combobox(formulario, values=nombres,
                                                state="disabled", width=37, style="TCombobox")
            self.combo_naturaleza.grid(row=1, column=1, pady=8)
            self.combo_naturaleza.set("Sin opciones")

            # Frame de filtro con combobox deshabilitado
            frame_filtro = tk.Frame(frame_titulo, bg=COLOR_PANEL)
            frame_filtro.pack(side="right")

            self.combo_filtro = ttk.Combobox(frame_filtro, values=nombres,
                                            state="disabled", width=15, style="TCombobox")
            self.combo_filtro.pack(side="left", padx=(0, 10), ipady=2)
            self.combo_filtro.set("Sin opciones")
            self.cargar_personas()
        else:
            nombres = [res[1] for res in resultado]

            self.combo_naturaleza = ttk.Combobox(formulario, values=nombres,
                                                state="readonly", width=37, style="TCombobox")
            self.combo_naturaleza.grid(row=1, column=1, pady=8)
            self.combo_naturaleza.current(0)

            # Frame de filtro al lado derecho del título
            frame_filtro = tk.Frame(frame_titulo, bg=COLOR_PANEL)
            frame_filtro.pack(side="right")

            self.combo_filtro = ttk.Combobox(frame_filtro, values=nombres,
                                            state="readonly", width=15, style="TCombobox")
            self.combo_filtro.pack(side="left", padx=(0, 10), ipady=2)

            if "Física" in nombres:
                self.combo_filtro.set("Física")
            else:
                self.combo_filtro.current(0)

            # Botón de aplicar filtro
            btn_aplicar_filtro = tk.Button(frame_filtro, text="Aplicar Filtro", 
                                        bg=COLOR_ACCION, fg=COLOR_TEXTO, 
                                        font=FUENTE_BOTON, relief=tk.FLAT,
                                        activebackground=COLOR_PRIMARIO_OSCURO,
                                        activeforeground=COLOR_TEXTO,
                                        command=self.aplicar_filtro)
            btn_aplicar_filtro.pack(side="left", ipadx=10, ipady=2)

            btn_aplicar_filtro.bind("<Enter>", lambda e: btn_aplicar_filtro.config(bg=COLOR_HOVER))
            btn_aplicar_filtro.bind("<Leave>", lambda e: btn_aplicar_filtro.config(bg=COLOR_ACCION))


        # Contenedor para la tabla con scroll
        frame_tabla = tk.Frame(panel, bg=COLOR_PANEL)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        # Tabla de personas con estilo personalizado
        columnas = ("id", "nombre", "naturaleza", "Es Cliente")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings",
                                 yscrollcommand=scrollbar.set)
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), anchor="w")
            self.tabla.column(col, width=150, anchor="w")
        
        self.tabla.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla.yview)

        self.cargar_personas()

            # Contenedor invisible para los botones
        boton_frame = tk.Frame(panel, bg=COLOR_PANEL)
        boton_frame.pack(pady=(5, 15))

        # Botón Guardar
        btn_guardar = tk.Button(boton_frame, text="Guardar Persona", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.guardar_persona)
        btn_guardar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_guardar.bind("<Enter>", lambda e: btn_guardar.config(bg=COLOR_HOVER))
        btn_guardar.bind("<Leave>", lambda e: btn_guardar.config(bg=COLOR_PRIMARIO))

        # Botón Eliminar
        btn_eliminar = tk.Button(boton_frame, text="Eliminar Persona", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.eliminar_persona)
        btn_eliminar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_eliminar.bind("<Enter>", lambda e: btn_eliminar.config(bg=COLOR_HOVER))
        btn_eliminar.bind("<Leave>", lambda e: btn_eliminar.config(bg=COLOR_PRIMARIO))

        # Botón actualizar
        btn_actualizar= tk.Button(boton_frame, text="Actualizar Persona", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.actualizar_persona)
        btn_actualizar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg=COLOR_HOVER))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg=COLOR_PRIMARIO))

        # Botón Buscar
        btn_buscar= tk.Button(boton_frame, text="Buscar Persona", 
                                bg=COLOR_PRIMARIO, fg=COLOR_TEXTO, 
                                font=FUENTE_BOTON, relief=tk.FLAT,
                                activebackground=COLOR_PRIMARIO_OSCURO,
                                activeforeground=COLOR_TEXTO,
                                command=self.buscar_persona)
        btn_buscar.pack(side="left", padx=10, ipadx=15, ipady=5)

        btn_buscar.bind("<Enter>", lambda e: btn_buscar.config(bg=COLOR_HOVER))
        btn_buscar.bind("<Leave>", lambda e: btn_buscar.config(bg=COLOR_PRIMARIO))

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
                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, valores[1])
                self.combo_naturaleza.set(valores[2])
                # Actualizar Radiobutton según el valor "Es Cliente"
                es_cliente_valor = valores[3]  # índice 3: "Es Cliente"
                if es_cliente_valor in ("Sí", "No"):
                    self.es_cliente_var.set(es_cliente_valor)
                else:
                    self.es_cliente_var.set("No")  # Por defecto si no está claro

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
        self.cargar_personas()
        self.id_seleccionado = None 
        self.entry_nombre.delete(0, tk.END)
        self.combo_naturaleza.set("")

    def cargar_personas(self):
        """Carga las personas en la tabla"""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        datos = self.party_model.mostrar_personas()

        if datos : 
            if isinstance(datos, list):
                for persona in datos:
                    self.tabla.insert('', 'end', values=persona)
            else:
                mensajes.mensajes_Error(f"No se pudieron cargar las personas:\n{datos}")

    def cargar_personas_filtros(self, contenido):
        """Carga las personas en la tabla"""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        if isinstance(contenido, list):
            for persona in contenido:
                self.tabla.insert('', 'end', values=persona)
        else:
           mensajes.mensajes_Error(f"No se pudieron carga la persona:\n{contenido}")


    def eliminar_persona(self): 
        self.party_model.eliminar_persona(self.id_seleccionado)
        

        self.limpiar()


    def actualizar_persona(self): 
        self.party_model.actualizar_party(self.id_seleccionado,self.entry_nombre.get(), self.combo_naturaleza.get())

        if self.id_seleccionado:
            es_cliente = self.es_cliente_var.get()
            if es_cliente == "Sí":
                controlador_cliente.hacer_cliente(self.id_seleccionado)
            else:
                controlador_cliente.eliminar_cliente(self.id_seleccionado)

            self.limpiar()
        self.limpiar()


    

    def buscar_persona(self): 
        resultado = self.party_model.buscar_party(self.entry_nombre.get())
        if resultado: 
            self.cargar_personas_filtros(resultado)
            return 
        self.limpiar()

    def aplicar_filtro(self):
        filtro = self.combo_filtro.get()
        resultado = controlador_party.filtrar_por_naturaleza(filtro)
        self.cargar_personas_filtros(resultado)

    def guardar_persona(self):
        nombre = self.entry_nombre.get()
        naturaleza = self.combo_naturaleza.get()
        party_id = controlador_party.guardar_persona(nombre, naturaleza)

        if party_id:
            es_cliente = self.es_cliente_var.get()
            if es_cliente == "Sí":
                controlador_cliente.hacer_cliente(party_id)
            else:
                controlador_cliente.eliminar_cliente(party_id)

            self.limpiar()

