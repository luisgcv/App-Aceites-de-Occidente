import tkinter as tk
from tkinter import ttk
from controllers import controlador_relacion_puesto, controlador_empleado, controlador_puesto
from utils.mensajes import mensajes

# Configuración de colores y fuentes
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
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")

class VentanaRelacionPuesto(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_relacion_puesto
        self.id_seleccionado = None

        self._configurar_estilos()
        self._construir_ui()
        self.cargar_datos()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", 
                         background=COLOR_FONDO, 
                         foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, 
                         borderwidth=0, 
                         font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", 
                         background=COLOR_BORDE, 
                         foreground=COLOR_TEXTO,
                         font=FUENTE_BOTON)
        estilo.map("Treeview", 
                  background=[("selected", COLOR_PRIMARIO_OSCURO)],
                  foreground=[("selected", COLOR_TEXTO)])
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


        # ─── CABECERA Y FILTROS A LA DERECHA ──────────────────────────
        cabecera = tk.Frame(panel, bg=COLOR_PANEL)
        cabecera.pack(fill="x", pady=(10, 10), padx=20)

        tk.Label(cabecera, text="Gestión Relación Empleado - Puesto",
                font=FUENTE_TITULO, bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")

        filtro_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        filtro_frame.pack(side="right")

        tk.Label(filtro_frame, text="Empleado:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        empleados = controlador_empleado.mostrar_nombre_completo()
        self.combo_filtro_empleado = self._crear_combo(filtro_frame, empleados)
        self.combo_filtro_empleado.config(width=15)
        self.combo_filtro_empleado.pack(side="left", padx=(0, 15), ipady=2, ipadx=30)

        tk.Label(filtro_frame, text="Puesto:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        puestos = controlador_puesto.mostrar_puestos()
        self.combo_filtro_puesto = self._crear_combo(filtro_frame, puestos)
        self.combo_filtro_puesto.config(width=15)
        self.combo_filtro_puesto.pack(side="left", padx=(0, 15), ipady=2, ipadx=30)

        btn_filtro = tk.Button(filtro_frame, text="Filtrar", bg=COLOR_ACCION, fg=COLOR_TEXTO,
                            font=FUENTE_BOTON, relief=tk.FLAT,
                            activebackground=COLOR_PRIMARIO_OSCURO,
                            activeforeground=COLOR_TEXTO,
                            command=self.aplicar_filtro)
        btn_filtro.pack(side="left")
        btn_filtro.bind("<Enter>", lambda e: btn_filtro.config(bg=COLOR_HOVER))
        btn_filtro.bind("<Leave>", lambda e: btn_filtro.config(bg=COLOR_ACCION))

        # Separador visual
        tk.Frame(panel, height=2, bg=COLOR_BORDE).pack(fill="x", padx=20, pady=(0, 10))

            # ─── FORMULARIO ───────────────────────────────────────────────
        form_wrapper = tk.Frame(panel, bg=COLOR_PANEL)
        form_wrapper.pack(fill="x", padx=20, pady=10)

        form = tk.Frame(form_wrapper, bg=COLOR_PANEL)
        form.pack(anchor="w", padx=10, pady=10)

        # Descripción (fila 0)
        tk.Label(form, text="Descripción:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_descripcion = tk.Entry(form, width=40, font=FUENTE_NORMAL, bg=COLOR_FONDO,
                                        fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                        relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                        highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_descripcion.grid(row=0, column=1, pady=6)

        # Empleado (fila 1)
        tk.Label(form, text="Empleado:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        self.combo_empleado = self._crear_combo(form, empleados)
        self.combo_empleado.grid(row=1, column=1, pady=6)

        # Puesto (fila 2)
        tk.Label(form, text="Puesto:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        self.combo_puesto = self._crear_combo(form, puestos)
        self.combo_puesto.grid(row=2, column=1, pady=6)



        # ─── TABLA ────────────────────────────────────────────────────
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scroll_y = ttk.Scrollbar(tabla_frame)
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        columnas = ("id", "empleado", "puesto", "descripcion")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings",
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=140 if col != "descripcion" else 250, anchor="w")

        self.tabla.pack(fill="both", expand=True)
        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)

        # ─── BOTONES ─────────────────────────────────────────────────
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=(5, 15))

        self._crear_boton(btn_frame, "Guardar", self.guardar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Actualizar", self.actualizar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Eliminar", self.eliminar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Buscar", self.buscar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Limpiar", self.limpiar).pack(side="left", padx=10)


    def _crear_boton(self, master, texto, comando):
        btn = tk.Button(master, text=f"{texto} Mecanismo", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                        font=FUENTE_BOTON, relief=tk.FLAT, activebackground=COLOR_PRIMARIO_OSCURO,
                        activeforeground=COLOR_TEXTO, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARIO))
        return btn


    # Resto de los métodos permanecen igual...
    def limpiar(self):
        self.id_seleccionado = None
        self.combo_empleado.set("")
        self.combo_puesto.set("")
        self.entry_descripcion.delete(0, tk.END)
        self.cargar_datos()

    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        datos = self.model.mostrar_relacion()
        if isinstance(datos, list):
            for fila in datos:
                self.tabla.insert("", "end", values=fila)
        elif datos is not None:
            mensajes.mensajes_Error(datos)

    def _seleccionar(self, _event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = int(valores[0])
            self.combo_empleado.set(valores[1])
            self.combo_puesto.set(valores[2])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[3])

    def guardar(self):
        self.model.guardar_relacion(
            self.combo_empleado.get(),
            self.combo_puesto.get(),
            self.entry_descripcion.get()
        )
        self.limpiar()

    def actualizar(self):
        self.model.actualizar_mecanismo(
            self.id_seleccionado,
            self.combo_empleado.get(),
            self.combo_puesto.get(),
            self.entry_descripcion.get()
        )
        self.limpiar()

    def eliminar(self):
        self.model.eliminar_relacion(self.id_seleccionado)
        self.limpiar()

    def buscar(self):
        resultados = self.model.buscar_relacion(self.combo_empleado.get())
        if resultados:
            self.tabla.delete(*self.tabla.get_children())
            if isinstance(resultados, list):
                for fila in resultados:
                    self.tabla.insert("", "end", values=fila)
                    
    def aplicar_filtro(self):
        empleado = self.combo_filtro_empleado.get()
        puesto = self.combo_filtro_puesto.get()

        resultados = self.model.filtrar_relacion(empleado, puesto)

        self.tabla.delete(*self.tabla.get_children())
        if isinstance(resultados, list):
            for fila in resultados:
                self.tabla.insert("", "end", values=fila)
        elif resultados is not None:
            mensajes.mensajes_Error(f"Error al aplicar filtro:\n{resultados}")