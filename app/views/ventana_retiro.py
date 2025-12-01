import tkinter as tk
from tkinter import Canvas, ttk
from tkcalendar import DateEntry
from controllers import controlador_retiro, controlador_empleado, controlador_banco
from utils.mensajes import mensajes

# Colores y fuentes
COLOR_FONDO = "#1B1F2A"
COLOR_PANEL = "#252B3A"
COLOR_TEXTO = "#FFFFFF"
COLOR_ACCION = "#4CAF50"
COLOR_HOVER = "#34D178"
COLOR_BORDE = "#34495E"
COLOR_PRIMARIO = "#2ECC71"
COLOR_PRIMARIO_OSCURO = "#27AE60"

FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")
FUENTE_TITULO = ("Segoe UI", 18, "bold")

class VentanaRetiro(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_retiro
        self.id_seleccionado = None
        self._configurar_estilos()
        self._construir_ui()
        self.cargar_retiros()
        self.bind_all("<MouseWheel>", lambda e: Canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", background=COLOR_BORDE, foreground=COLOR_TEXTO,
                         font=FUENTE_BOTON)
        estilo.map("Treeview", background=[("selected", COLOR_PRIMARIO_OSCURO)])
        estilo.configure("TCombobox", fieldbackground=COLOR_FONDO, background=COLOR_FONDO,
                         foreground=COLOR_TEXTO)

    def _crear_combo(self, master, datos):
        nombres = [d[1] if isinstance(d, (list, tuple)) else d for d in datos] if datos else []
        combo = ttk.Combobox(master, values=nombres, state="readonly" if nombres else "disabled", width=37)
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

        # Cabecera
        cabecera = tk.Frame(panel, bg=COLOR_PANEL)
        cabecera.pack(fill="x", pady=(10, 10), padx=20)
        tk.Label(cabecera, text="Gestión Retiros", font=FUENTE_TITULO,
                 bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")

        form = tk.Frame(panel, bg=COLOR_PANEL)
        form.pack(anchor="w", padx=20, pady=10)

        # Filtros
        filtro_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        filtro_frame.pack(side="right")

        # Fecha Desde
        tk.Label(filtro_frame, text="Desde:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_fecha_inicio = DateEntry(filtro_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.filtro_fecha_inicio.pack(side="left", padx=(0, 10))

        # Fecha Hasta
        tk.Label(filtro_frame, text="Hasta:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_fecha_fin = DateEntry(filtro_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.filtro_fecha_fin.pack(side="left", padx=(0, 10))

        # Empleado
        tk.Label(filtro_frame, text="Empleado:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        empleados = controlador_empleado.mostrar_nombre_completo()
        nombres_empleados = [e[1] for e in empleados]
        self.combo_filtro_empleado = ttk.Combobox(filtro_frame, values=nombres_empleados, state="readonly", width=25)
        self.combo_filtro_empleado.set("")  # iniciar vacío
        self.combo_filtro_empleado.pack(side="left", padx=(0, 10))

        # Botón Filtrar
        btn_filtro = tk.Button(filtro_frame, text="Filtrar", bg=COLOR_ACCION, fg=COLOR_TEXTO,
                               font=FUENTE_BOTON, relief=tk.FLAT,
                               activebackground=COLOR_PRIMARIO_OSCURO,
                               activeforeground=COLOR_TEXTO,
                               command=self.aplicar_filtro)
        btn_filtro.pack(side="left")
        btn_filtro.bind("<Enter>", lambda e: btn_filtro.config(bg=COLOR_HOVER))
        btn_filtro.bind("<Leave>", lambda e: btn_filtro.config(bg=COLOR_ACCION))


        # Campos
        self._agregar_label_entry(form, "Descripción:", 0)
        self.entry_descripcion = self._crear_entry(form, 0)

        self._agregar_label_entry(form, "Monto:", 1)
        self.entry_monto = self._crear_entry(form, 1)

        tk.Label(form, text="Fecha:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="w", pady=6)
        self.entry_fecha = DateEntry(form, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd',
                                     background='darkblue', foreground='white', borderwidth=2)
        self.entry_fecha.grid(row=2, column=1, pady=6)

        tk.Label(form, text="Empleado:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=3, column=0, sticky="w", pady=6)
        empleados = controlador_empleado.mostrar_nombre_completo()
        self.combo_empleado = self._crear_combo(form, empleados)
        self.combo_empleado.grid(row=3, column=1, pady=6)

        tk.Label(form, text="Banco:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=4, column=0, sticky="w", pady=6)
        bancos = controlador_banco.traer_cuenta_iban()
        self.combo_banco = self._crear_combo(form, bancos)
        self.combo_banco.grid(row=4, column=1, pady=6)

        # Tabla
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)
        scroll = ttk.Scrollbar(tabla_frame)
        scroll.pack(side="right", fill="y")

        columnas = ("id", "descripcion", "monto", "fecha", "banco", "empleado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", yscrollcommand=scroll.set)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, anchor="center", width=120)
        self.tabla.pack(fill="both", expand=True)

        # Total Retiros
        self.total_label = tk.Label(panel, text="Total Retiros: ₡0.00", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        self.total_label.pack(pady=(5, 10), anchor="e", padx=20)

        scroll.config(command=self.tabla.yview)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # Botones
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=(5, 15))
        self._crear_boton(btn_frame, "Guardar", self.guardar_retiro).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Actualizar", self.actualizar_retiro).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Eliminar", self.eliminar_retiro).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Limpiar", self.limpiar).pack(side="left", padx=10)

    def _agregar_label_entry(self, parent, texto, fila):
        tk.Label(parent, text=texto, font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=fila, column=0, sticky="w", pady=6, padx=(0, 10))

    def _crear_entry(self, parent, fila):
        entry = tk.Entry(parent, width=40, font=FUENTE_NORMAL, bg=COLOR_FONDO,
                         fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                         relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                         highlightthickness=1, highlightbackground=COLOR_BORDE)
        entry.grid(row=fila, column=1, pady=6)
        return entry

    def _crear_boton(self, master, texto, comando):
        btn = tk.Button(master, text=f"{texto} Retiro", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                        font=FUENTE_BOTON, relief=tk.FLAT, activebackground=COLOR_PRIMARIO_OSCURO,
                        activeforeground=COLOR_TEXTO, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARIO))
        return btn

    def limpiar(self):
        self.id_seleccionado = None
        for entry in [self.entry_descripcion, self.entry_monto, self.entry_fecha]:
            entry.delete(0, tk.END)
        self.combo_empleado.current(0)
        self.combo_banco.current(0)
        self.cargar_retiros()

    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            val = self.tabla.item(item, "values")
            self.id_seleccionado = val[0]
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, val[1])
            self.entry_monto.delete(0, tk.END)
            self.entry_monto.insert(0, val[2])
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, val[3])
            self.combo_banco.set(val[4])
            self.combo_empleado.set(val[5])

    def cargar_retiros(self):
        self.tabla.delete(*self.tabla.get_children())
        datos = self.model.mostrar_retiro()
        if isinstance(datos, list):
            for fila in datos:
                self.tabla.insert("", "end", values=fila)

        self.actualizar_total_retiros()


    def guardar_retiro(self):
        self.model.guardar_retiro(
            self.entry_descripcion.get(),
            self.entry_monto.get(),
            self.entry_fecha.get(),
            self.combo_empleado.get(),
            self.combo_banco.get()
        )
        self.limpiar()

    def actualizar_retiro(self):
        self.model.actualizar_retiro(
            self.id_seleccionado,
            self.entry_descripcion.get(),
            self.entry_monto.get(),
            self.entry_fecha.get(),
            self.combo_empleado.get(),
            self.combo_banco.get()
        )
        self.limpiar()

    def eliminar_retiro(self):
        self.model.eliminar_retiro(self.id_seleccionado)
        self.limpiar()

    def aplicar_filtro(self):
        fecha_inicio = self.filtro_fecha_inicio.get()
        fecha_fin = self.filtro_fecha_fin.get()
        empleado = self.combo_filtro_empleado.get()

 

        resultados = self.model.filtrar_retiro(fecha_inicio, fecha_fin, empleado)

        self.tabla.delete(*self.tabla.get_children())
        if isinstance(resultados, list):
            for fila in resultados:
                self.tabla.insert("", "end", values=fila)
        self.actualizar_total_retiros()



    def actualizar_total_retiros(self):
        total = 0
        for child in self.tabla.get_children():
            monto_str = self.tabla.item(child)["values"][2]  # columna monto
            try:
                monto = float(monto_str)
                total += monto
            except (ValueError, TypeError):
                pass

        self.total_label.config(text=f"Total Retiros: ₡{total:,.2f}")
