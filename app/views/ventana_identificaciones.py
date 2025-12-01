import tkinter as tk
from tkinter import ttk
from controllers import controlador_identificacion, controlador_tipo_identificaciones, controlador_nacionalidad, controlador_party
from utils.mensajes import mensajes

# Colores y fuentes (igual que tu ventana Party)
COLOR_FONDO = "#1B1F2A"
COLOR_PANEL = "#252B3A"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_SEC = "#B0B4C8"
COLOR_PRIMARIO = "#2ECC71"
COLOR_PRIMARIO_OSCURO = "#27AE60"
COLOR_HOVER = "#34D178"
COLOR_ACCION = "#4CAF50"
COLOR_BORDE = "#34495E"

FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 14)
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")
FUENTE_MENU = ("Segoe UI", 11)

class VentanaIdentificacion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_identificacion
        self.id_seleccionado = None

        self._configurar_estilos()
        self._construir_ui()
        self.cargar_identificaciones()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, borderwidth=0, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", background=COLOR_BORDE, foreground=COLOR_TEXTO,
                         font=FUENTE_BOTON, relief="flat")
        estilo.map("Treeview", background=[("selected", COLOR_PRIMARIO_OSCURO)],
                   foreground=[("selected", COLOR_TEXTO)])
        estilo.configure("TSeparator", background=COLOR_BORDE)

        # Estilo para Combobox
        estilo.configure("TCombobox",
                         fieldbackground=COLOR_FONDO,
                         background=COLOR_FONDO,
                         foreground=COLOR_TEXTO,
                         selectbackground=COLOR_PRIMARIO_OSCURO,
                         selectforeground=COLOR_TEXTO)

    def _crear_combo(self, master, datos):
        estilo_combo = ttk.Style()
        estilo_combo.theme_use("clam")  # Importante para que los colores funcionen correctamente
        estilo_combo.configure("TCombobox",
            foreground=COLOR_BORDE,
            background=COLOR_PANEL,
            fieldbackground=COLOR_FONDO,
            selectbackground=COLOR_PRIMARIO_OSCURO,
            selectforeground=COLOR_TEXTO,
            bordercolor=COLOR_BORDE,
            lightcolor=COLOR_BORDE,
            darkcolor=COLOR_BORDE
        )

        nombres = [d[1] if isinstance(d, (list, tuple)) else d for d in datos] if datos else []
        estado = "readonly" if nombres else "disabled"

        combo = ttk.Combobox(master, values=nombres, state=estado, width=37, style="TCombobox")

        if nombres:
            combo.current(0)
        else:
            combo.set("Sin opciones")  # Este texto sí se verá con color si configuraste correctamente

        return combo


    def _construir_ui(self):
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


        cabecera = tk.Frame(panel, bg=COLOR_PANEL)
        cabecera.pack(fill="x", pady=(10, 10), padx=20)
        tk.Label(cabecera, text="Gestión de Identificaciones", font=FUENTE_TITULO,
                 bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")
        tk.Frame(cabecera, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(5, 0))

        form_wrapper = tk.Frame(panel, bg=COLOR_PANEL)
        form_wrapper.pack(fill="x", padx=20, pady=10)
        form = tk.Frame(form_wrapper, bg=COLOR_PANEL)
        form.pack(anchor="w", padx=10, pady=10)

        # Valor
        tk.Label(form, text="Valor:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_valor = tk.Entry(form, width=40, font=FUENTE_NORMAL, bg=COLOR_FONDO,
                                   fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                   relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                   highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_valor.grid(row=0, column=1, pady=6)

        # Tipo Identificacion
        tk.Label(form, text="Tipo identificación:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        tipos = controlador_tipo_identificaciones.mostrar_tipos_identificacion()
        self.combo_tipo = self._crear_combo(form, tipos)
        self.combo_tipo.grid(row=1, column=1, pady=6)

        # Nacionalidad
        tk.Label(form, text="Nacionalidad:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        nacionalidades = controlador_nacionalidad.mostrar_nacionalidad()
        self.combo_nacionalidad = self._crear_combo(form, nacionalidades)
        self.combo_nacionalidad.grid(row=2, column=1, pady=6)

        # Persona / Party
        tk.Label(form, text="Persona:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=3, column=0, sticky="w", pady=6, padx=(0, 10))
        parties = controlador_party.mostrar_personas()
        self.combo_party = self._crear_combo(form, parties)
        self.combo_party.grid(row=3, column=1, pady=6)


        # Frame filtros (parte derecha)
        filtro_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        filtro_frame.pack(side="right")

        # Filtro por Tipo Identificación
        tk.Label(filtro_frame, text="Tipo:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        tipos = controlador_tipo_identificaciones.mostrar_tipos_identificacion()
        self.combo_filtro_tipo = self._crear_combo(filtro_frame, tipos)
        self.combo_filtro_tipo.config(width=15)
        self.combo_filtro_tipo.pack(side="left", padx=(0, 15), ipady=2, ipadx=30)

        # Filtro por Party (Nombre)
        tk.Label(filtro_frame, text="Persona:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        parties = controlador_party.mostrar_personas()
        self.combo_filtro_party = self._crear_combo(filtro_frame, parties)
        self.combo_filtro_party.config(width=15)
        self.combo_filtro_party.pack(side="left", padx=(0, 15), ipady=2, ipadx=30)

        # Botón Aplicar Filtro
        btn_filtro = tk.Button(filtro_frame, text="Filtrar", bg=COLOR_ACCION, fg=COLOR_TEXTO,
                            font=FUENTE_BOTON, relief=tk.FLAT,
                            activebackground=COLOR_PRIMARIO_OSCURO,
                            activeforeground=COLOR_TEXTO,
                            command=self.aplicar_filtro)
        btn_filtro.pack(side="left")
        btn_filtro.bind("<Enter>", lambda e: btn_filtro.config(bg=COLOR_HOVER))
        btn_filtro.bind("<Leave>", lambda e: btn_filtro.config(bg=COLOR_ACCION))


        # Tabla con scrollbar
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        scroll = ttk.Scrollbar(tabla_frame)
        scroll.pack(side="right", fill="y")
        columnas = ("id", "valor", "tipo_identificacion", "nacionalidad", "nombre_party")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings",
                                  yscrollcommand=scroll.set)
        for col in columnas:
            self.tabla.heading(col, text=col.replace("_", " ").capitalize(), anchor="w")
            self.tabla.column(col, width=140, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # Botones
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=(5, 15))
        self._crear_boton(btn_frame, "Guardar", self.guardar_identificacion).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Actualizar", self.actualizar_identificacion).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Eliminar", self.eliminar_identificacion).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Buscar", self.buscar_identificacion).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Limpiar", self.limpiar).pack(side="left", padx=10)

    def _crear_boton(self, master, texto, comando):
        btn = tk.Button(master, text=f"{texto} Identificación", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                        font=FUENTE_BOTON, relief=tk.FLAT, activebackground=COLOR_PRIMARIO_OSCURO,
                        activeforeground=COLOR_TEXTO, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARIO))
        return btn

    def limpiar(self):
        self.id_seleccionado = None
        self.entry_valor.delete(0, tk.END)
        for combo in (self.combo_tipo, self.combo_nacionalidad, self.combo_party):
            if combo["state"] == "readonly":
                combo.current(0)
            else:
                combo.set("")
        self.cargar_identificaciones()

    def cargar_identificaciones(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        datos = self.model.mostrar_identificaciones()
        if isinstance(datos, list):
            for item in datos:
                self.tabla.insert("", "end", values=item)
        elif datos is not None:
            mensajes.mensajes_Error(f"No se pudieron cargar las identificaciones:\n{datos}")

    def _al_seleccionar(self, _event):
        item = self.tabla.focus()
        if item:
            val = self.tabla.item(item, "values")
            self.id_seleccionado = int(val[0])
            self.entry_valor.delete(0, tk.END)
            self.entry_valor.insert(0, val[1])
            self.combo_tipo.set(val[2])
            self.combo_nacionalidad.set(val[3] or "")
            self.combo_party.set(val[4])

    def guardar_identificacion(self):
        self.model.guardar_identificacion(
            self.entry_valor.get(),
            self.combo_tipo.get(),
            self.combo_nacionalidad.get(),
            self.combo_party.get()
        )
        self.limpiar()

    def actualizar_identificacion(self):
        self.model.actualizar_party(
            self.id_seleccionado,
            self.entry_valor.get(),
            self.combo_tipo.get(),
            self.combo_nacionalidad.get(),
            self.combo_party.get()
        )
        self.limpiar()

    def eliminar_identificacion(self):
        self.model.eliminar_identificacion(self.id_seleccionado)
        self.limpiar()

    def buscar_identificacion(self):
        datos = self.model.buscar_identificacion(self.combo_party.get())
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        if isinstance(datos, list):
            for item in datos:
                self.tabla.insert("", "end", values=item)
        else:
            self.limpiar()


    def aplicar_filtro(self):
        tipo = self.combo_filtro_tipo.get()
        nombre = self.combo_filtro_party.get()
        
        resultados = self.model.filtrar_identificaciones(tipo, nombre)  # Este método lo defines después en el modelo

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        if isinstance(resultados, list):
            for item in resultados:
                self.tabla.insert("", "end", values=item)
        elif resultados is not None:
            mensajes.mensajes_Error(f"Error al filtrar:\n{resultados}")
