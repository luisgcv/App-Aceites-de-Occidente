import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date

from controllers import controlador_ingreso, controlador_factura
from utils import mensajes

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


class VentanaIngresos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_ingreso
        self.id_seleccionado = None

        self._configurar_estilos()
        self._construir_ui()
        self.cargar_ingresos()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, borderwidth=0, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", background=COLOR_BORDE, foreground=COLOR_TEXTO,
                         font=FUENTE_BOTON, relief="flat")
        estilo.map("Treeview", background=[("selected", COLOR_PRIMARIO_OSCURO)],
                   foreground=[("selected", COLOR_TEXTO)])


    def _crear_combo(self, master, datos):
        estilo_combo = ttk.Style()
        estilo_combo.theme_use("clam") 
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
        container = tk.Frame(self, bg=COLOR_FONDO)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        panel = tk.Frame(container, bg=COLOR_PANEL, bd=2, relief=tk.GROOVE)
        panel.pack(fill="both", expand=True)

        # Cabecera
        cabecera = tk.Frame(panel, bg=COLOR_PANEL)
        cabecera.pack(fill="x", pady=10, padx=20)
        tk.Label(cabecera, text="Gestión de Ingresos", font=FUENTE_TITULO,
                 bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")

        filtro_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        filtro_frame.pack(side="right")

        tk.Label(filtro_frame, text="Desde:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_fecha_inicio = DateEntry(filtro_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.filtro_fecha_inicio.pack(side="left", padx=(0, 10))

        tk.Label(filtro_frame, text="Hasta:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_fecha_fin = DateEntry(filtro_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.filtro_fecha_fin.pack(side="left", padx=(0, 10))

        btn_filtro = tk.Button(filtro_frame, text="Filtrar", bg=COLOR_ACCION, fg=COLOR_TEXTO,
                               font=FUENTE_BOTON, relief=tk.FLAT,
                               activebackground=COLOR_PRIMARIO_OSCURO,
                               activeforeground=COLOR_TEXTO,
                               command=self.aplicar_filtro)
        btn_filtro.pack(side="left")
        btn_filtro.bind("<Enter>", lambda e: btn_filtro.config(bg=COLOR_HOVER))
        btn_filtro.bind("<Leave>", lambda e: btn_filtro.config(bg=COLOR_ACCION))

        # Formulario
        form = tk.Frame(panel, bg=COLOR_PANEL)
        form.pack(fill="x", padx=20, pady=10)

        # Fila 0
        tk.Label(form, text="Número Factura:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=0, sticky="w", pady=6)
        facturas = controlador_factura.mostrar_numero_factura()
        self.combo_factura = self._crear_combo(form, facturas)
        self.combo_factura.grid(row=0, column=1, pady=6, padx=(0, 10), sticky="ew")

        tk.Label(form, text="Fecha:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=2, sticky="w", padx=(10, 10))
        self.fecha = DateEntry(form, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.fecha.grid(row=0, column=3, pady=6, sticky="ew")

        # Fila 1
        tk.Label(form, text="Monto:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=0, sticky="w", pady=6)
        self.entry_monto = tk.Entry(form, font=FUENTE_NORMAL)
        self.entry_monto.grid(row=1, column=1, pady=6, padx=(0, 10), sticky="ew")

        tk.Label(form, text="Descripción:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=2, sticky="w", padx=(10, 10))
        self.entry_descripcion = tk.Entry(form, font=FUENTE_NORMAL)
        self.entry_descripcion.grid(row=1, column=3, pady=6, sticky="ew")

        # Tabla
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        scroll = ttk.Scrollbar(tabla_frame)
        scroll.pack(side="right", fill="y")

        columnas = ("id", "fecha", "monto", "descripcion", "numero_factura")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", yscrollcommand=scroll.set)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), anchor="w")
            self.tabla.column(col, width=120, anchor="w")

        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)

        self.tabla.pack(fill="both", expand=True)

        # Total Ingreso
        self.total_label = tk.Label(panel, text="Total Ingresos: ₡0.00", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        self.total_label.pack(pady=(5, 10), anchor="e", padx=20)

        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # Botones
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=10)
        self._crear_boton(btn_frame, "Guardar", self.guardar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Actualizar", self.actualizar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Eliminar", self.eliminar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Limpiar", self.limpiar).pack(side="left", padx=10)

    def _crear_boton(self, master, texto, comando):
        btn = tk.Button(master, text=texto, bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                        font=FUENTE_BOTON, relief=tk.FLAT, activebackground=COLOR_PRIMARIO_OSCURO,
                        activeforeground=COLOR_TEXTO, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARIO))
        return btn

    def cargar_ingresos(self):
        self.tabla.delete(*self.tabla.get_children())
        datos = self.model.mostrar_factura()
        if isinstance(datos, list):
            for fila in datos:
                self.tabla.insert("", "end", values=fila)

        self.actualizar_total_ingreso()

    def aplicar_filtro(self):
        inicio = self.filtro_fecha_inicio.get()
        fin = self.filtro_fecha_fin.get()
        datos = self.model.filtrar_ingreso(inicio, fin)
        self.tabla.delete(*self.tabla.get_children())
        if isinstance(datos, list):
            for fila in datos:
                self.tabla.insert("", "end", values=fila)
        self.actualizar_total_ingreso()


    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = valores[0]
            self.fecha.set_date(valores[1])
            self.entry_monto.delete(0, tk.END)
            self.entry_monto.insert(0, valores[2])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[3])
            self.combo_factura.set(valores[4])

    def guardar(self):

        self.model.guardar_ingreso(
            self.combo_factura.get(),
            self.entry_monto.get(),
            self.fecha.get(),
            self.entry_descripcion.get()
        )
        self.limpiar()

    def actualizar(self):
        self.model.actualizar_ingreso(
            self.id_seleccionado,
            self.combo_factura.get(),
            self.entry_monto.get(),
            self.fecha.get(),
            self.entry_descripcion.get()
        )
        self.limpiar()

    def eliminar(self):
        self.model.eliminar_factura(self.id_seleccionado,self.combo_factura.get())
        self.limpiar()

    def limpiar(self):
        self.id_seleccionado = None
        self.combo_factura.set("")
        self.entry_monto.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.fecha.set_date(date.today())
        self.cargar_ingresos()

        
    def actualizar_total_ingreso(self):
        total = 0
        for child in self.tabla.get_children():
            monto_str = self.tabla.item(child)["values"][2]  # columna monto
            try:
                monto = float(monto_str)
                total += monto
            except (ValueError, TypeError):
                pass

        self.total_label.config(text=f"Total Ingreso: ₡{total:,.2f}")
