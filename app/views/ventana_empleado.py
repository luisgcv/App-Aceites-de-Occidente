import tkinter as tk
from tkinter import Canvas, ttk
from controllers import controlador_empleado, controlador_party
from utils.mensajes import mensajes
from tkcalendar import DateEntry



# ─── Estilos de Colores y Fuentes ──────────────────────────
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

class VentanaEmpleado(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_empleado
        self.id_seleccionado = None
        self._configurar_estilos()
        self._construir_ui()
        self.cargar_empleados()


    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", background=COLOR_BORDE, foreground=COLOR_TEXTO,
                         font=FUENTE_BOTON)
        estilo.map("Treeview", background=[("selected", COLOR_PRIMARIO_OSCURO)])

        estilo.configure("TCombobox",
                         fieldbackground=COLOR_FONDO,
                         background=COLOR_FONDO,
                         foreground=COLOR_TEXTO,
                         selectbackground=COLOR_PRIMARIO_OSCURO,
                         selectforeground=COLOR_TEXTO)

    def _crear_combo(self, master, datos):

        nombres = [d[1] if isinstance(d, (list, tuple)) else d for d in datos] if datos else []
        estado = "readonly" if nombres else "disabled"

        combo = ttk.Combobox(master, values=nombres, state=estado, width=37, style="TCombobox")
        combo.set(nombres[0] if nombres else "Sin opciones")
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

        tk.Label(cabecera, text="Gestión Empleados", font=FUENTE_TITULO,
                bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")

        filtro_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        filtro_frame.pack(side="right")

        # Filtro por nombre completo
        tk.Label(filtro_frame, text="Nombre completo:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))

        empleados = controlador_empleado.mostrar_nombre_completo()
        self.combo_filtro_nombre = self._crear_combo(filtro_frame, empleados)
        self.combo_filtro_nombre.config(width=25)
        self.combo_filtro_nombre.pack(side="left", padx=(0, 15), ipady=2, ipadx=30)

        # Botón de aplicar filtro
        btn_filtro = tk.Button(filtro_frame, text="Filtrar", bg=COLOR_ACCION, fg=COLOR_TEXTO,
                            font=FUENTE_BOTON, relief=tk.FLAT,
                            activebackground=COLOR_PRIMARIO_OSCURO,
                            activeforeground=COLOR_TEXTO,
                            command=self.aplicar_filtro)
        btn_filtro.pack(side="left")
        btn_filtro.bind("<Enter>", lambda e: btn_filtro.config(bg=COLOR_HOVER))
        btn_filtro.bind("<Leave>", lambda e: btn_filtro.config(bg=COLOR_ACCION))


        form_wrapper = tk.Frame(panel, bg=COLOR_PANEL)
        form_wrapper.pack(fill="x", padx=20, pady=10)
        form = tk.Frame(form_wrapper, bg=COLOR_PANEL)
        form.pack(anchor="w", padx=10, pady=10)

        # Primer Apellido
        tk.Label(form, text="Primer Apellido:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_primer_apellido = tk.Entry(form, width=40, font=FUENTE_NORMAL, bg=COLOR_FONDO,
                                   fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                   relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                   highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_primer_apellido.grid(row=0, column=1, pady=6)

        # Segundo Apellido
        tk.Label(form, text="Segundo Apellido:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_segundo_apellido = tk.Entry(form, width=40, font=FUENTE_NORMAL, bg=COLOR_FONDO,
                                   fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                   relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                   highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_segundo_apellido.grid(row=1, column=1, pady=6)

        # Fecha Nacimiento
        tk.Label(form, text="Fecha Nacimiento:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_fecha_nacimiento = DateEntry(form,  
                                        font=FUENTE_NORMAL, 
                                        date_pattern='yyyy-mm-dd', 
                                        background='darkblue', 
                                        foreground='white', 
                                        borderwidth=2,
                                        maxdate=None)  # puedes poner maxdate=date.today() si deseas restringir
        self.entry_fecha_nacimiento.grid(row=2, column=1, pady=6)



        # Combo Party
        tk.Label(form, text="Persona (Party):", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=3, column=0, sticky="w", pady=6, padx=(0, 10))
        parties = controlador_party.mostrar_personas()
        self.combo_party = self._crear_combo(form, parties)
        self.combo_party.grid(row=3, column=1, pady=6)

        # Tabla
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        scroll = ttk.Scrollbar(tabla_frame)
        scroll.pack(side="right", fill="y")

        columnas = ("id", "primer_apellido", "segundo_apellido", "fecha_nacimiento", "party_nombre")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", yscrollcommand=scroll.set)
        for col in columnas:
            self.tabla.heading(col, text=col.replace("_", " ").capitalize())
            self.tabla.column(col, anchor="center", width=140)
        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # Botones
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=(5, 15))
        self._crear_boton(btn_frame, "Guardar", self.guardar_empleado).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Actualizar", self.actualizar_empleado).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Eliminar", self.eliminar_empleado).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Buscar", self.buscar_empleado).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Limpiar", self.limpiar).pack(side="left", padx=10)

    def _crear_boton(self, master, texto, comando):
        btn = tk.Button(master, text=f"{texto} Empleado", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                        font=FUENTE_BOTON, relief=tk.FLAT, activebackground=COLOR_PRIMARIO_OSCURO,
                        activeforeground=COLOR_TEXTO, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARIO))
        return btn

    def limpiar(self):
        self.id_seleccionado = None
        self.entry_primer_apellido.delete(0, tk.END)
        self.entry_segundo_apellido.delete(0, tk.END)
        self.entry_fecha_nacimiento.delete(0, tk.END)
        if self.combo_party["state"] == "readonly":
            self.combo_party.current(0)
        self.cargar_empleados()

    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            val = self.tabla.item(item, "values")
            self.id_seleccionado = val[0]
            self.entry_primer_apellido.delete(0, tk.END)
            self.entry_primer_apellido.insert(0, val[1])
            self.entry_segundo_apellido.delete(0, tk.END)
            self.entry_segundo_apellido.insert(0, val[2])
            self.entry_fecha_nacimiento.delete(0, tk.END)
            self.entry_fecha_nacimiento.insert(0, val[3])
            self.combo_party.set(val[4])

    def cargar_empleados(self):
        self.tabla.delete(*self.tabla.get_children())
        datos = self.model.mostrar_empleados()
        if isinstance(datos, list):
            for fila in datos:
                self.tabla.insert("", "end", values=fila)

    def guardar_empleado(self):
        self.model.guardar_empleado(
            self.entry_primer_apellido.get(),
            self.entry_segundo_apellido.get(),
            self.entry_fecha_nacimiento.get(),
            self.combo_party.get()
        )
        self.limpiar()

    def actualizar_empleado(self):
        self.model.actualizar_empleado(
            self.id_seleccionado,
            self.entry_primer_apellido.get(),
            self.entry_segundo_apellido.get(),
            self.entry_fecha_nacimiento.get(),
            self.combo_party.get()
        )
        self.limpiar()

    def eliminar_empleado(self):
        self.model.eliminar_empleado(self.id_seleccionado)
        self.limpiar()

    def buscar_empleado(self):
        datos = self.model.buscar_empleado(self.entry_primer_apellido.get(),self.entry_segundo_apellido.get())
        if not datos: 
            return
        self.tabla.delete(*self.tabla.get_children())
        if isinstance(datos, list):
            for fila in datos:
                self.tabla.insert("", "end", values=fila)


    def aplicar_filtro(self):
        
        # Llamar al método del modelo para buscar por nombre completo
        datos = self.model.buscar_por_nombre_completo(self.combo_filtro_nombre.get())

        self.tabla.delete(*self.tabla.get_children())
        if isinstance(datos, list) and datos:
            for fila in datos:
                self.tabla.insert("", "end", values=fila)

