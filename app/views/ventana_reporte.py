import tkinter as tk
from tkinter import ttk
from controllers import controlador_reporte,controlador_empleado
from utils.pdf.pdf_exporter import exportar_pdf
from utils.mensajes import mensajes
from tkcalendar import DateEntry

# Actualiza estos colores para un look más moderno
COLOR_FONDO = "#0F172A"  # Azul oscuro más intenso
COLOR_PANEL = "#1E293B"   # Panel ligeramente más claro que el fondo
COLOR_TEXTO = "#E2E8F0"   # Texto más suave
COLOR_TEXTO_SEC = "#94A3B8"  # Texto secundario
COLOR_PRIMARIO = "#3B82F6"   # Azul moderno en lugar de verde
COLOR_PRIMARIO_OSCURO = "#2563EB"
COLOR_HOVER = "#60A5FA"      # Azul más claro para hover
COLOR_ACCION = "#10B981"     # Verde para acciones positivas
COLOR_BORDE = "#334155"      # Borde más suave

# Fuentes más modernas
FUENTE_TITULO = ("Segoe UI", 16, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 12, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
FUENTE_BOTON = ("Segoe UI", 10, "bold")


class VentanaReportes(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.reporte_actual = None
        self.resultados = []
        self.campos_dinamicos = {}

        self._configurar_estilos()
        self._construir_ui()


    def _crear_combo(self, master, datos):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TCombobox",
            foreground=COLOR_TEXTO,
            background=COLOR_PANEL,
            fieldbackground=COLOR_PANEL,
            selectbackground=COLOR_PRIMARIO_OSCURO,
            selectforeground=COLOR_TEXTO,
            bordercolor=COLOR_BORDE,
            lightcolor=COLOR_BORDE,
            darkcolor=COLOR_BORDE,
            arrowsize=12,
            padding=5,
            relief="flat",
            font=FUENTE_NORMAL
        )
        
        nombres = [d[1] if isinstance(d, (list, tuple)) else d for d in datos] if datos else []
        estado = "readonly" if nombres else "disabled"
        
        combo = ttk.Combobox(
            master, 
            values=nombres, 
            state=estado, 
            width=35, 
            style="Custom.TCombobox"
        )
        
        if nombres:
            combo.current(0)
        else:
            combo.set("No hay opciones disponibles")
        
        return combo


    def _configurar_estilos(self):
        style = ttk.Style()
        
        # Estilo para la tabla
        style.configure("Custom.Treeview",
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO,
            fieldbackground=COLOR_PANEL,
            borderwidth=0,
            font=FUENTE_NORMAL,
            rowheight=25
        )
        style.configure("Custom.Treeview.Heading",
            background=COLOR_BORDE,
            foreground=COLOR_TEXTO,
            font=FUENTE_BOTON,
            relief="flat",
            padding=5
        )
        style.map("Custom.Treeview",
            background=[("selected", COLOR_PRIMARIO_OSCURO)],
            foreground=[("selected", COLOR_TEXTO)]
        )
        
        # Estilo para el scrollbar
        style.configure("Custom.Vertical.TScrollbar",
            gripcount=0,
            background=COLOR_BORDE,
            darkcolor=COLOR_BORDE,
            lightcolor=COLOR_BORDE,
            troughcolor=COLOR_PANEL,
            bordercolor=COLOR_PANEL,
            arrowcolor=COLOR_TEXTO,
            arrowsize=12
        )

    def _cargar_tabla(self, datos, nombres_columnas=None):
        self.tabla.delete(*self.tabla.get_children())
        
        if not datos:
            self.tabla["columns"] = []
            return
        
        if nombres_columnas is None:
            columnas = list(range(len(datos[0])))
            nombres_columnas = [f"Columna {i+1}" for i in columnas]
        
        self.tabla["columns"] = nombres_columnas
        
        for col in nombres_columnas:
            self.tabla.heading(col, text=col, anchor="center")
            # Ajuste automático del ancho de columnas
            self.tabla.column(col, width=tk.font.Font().measure(col) + 20, anchor="center", minwidth=50)
        
        for fila in datos:
            self.tabla.insert("", "end", values=fila if isinstance(fila, (list, tuple)) else [fila])
        
        # Ajustar el ancho de las columnas según el contenido
        for col in nombres_columnas:
            max_width = tk.font.Font().measure(col)
            for row in datos:
                cell_width = tk.font.Font().measure(str(row[nombres_columnas.index(col)] if isinstance(row, (list, tuple)) else str(row)))
                if cell_width > max_width:
                    max_width = cell_width
            self.tabla.column(col, width=max_width + 20)
            
        
    def _construir_ui(self):
        # Contenedor principal con sombra
        container = tk.Frame(self, bg=COLOR_FONDO)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel con efecto de elevación
        panel = tk.Frame(container, bg=COLOR_PANEL, bd=0, 
                        highlightbackground="#475569", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Cabecera con mejor diseño
        cabecera = tk.Frame(panel, bg=COLOR_PANEL)
        cabecera.pack(fill="x", pady=(15, 10), padx=15)
        
        # Título con icono (puedes añadir un icono real si lo deseas)
        titulo_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        titulo_frame.pack(side="left")
        tk.Label(titulo_frame, text="📊 ", font=FUENTE_TITULO, 
                bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")
        tk.Label(titulo_frame, text="Reportes Generales", font=FUENTE_TITULO,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=5)
        
        # Combo de reportes con mejor estilo
        self.combo_reportes = ttk.Combobox(
            cabecera, 
            state="readonly", 
            width=35, 
            font=FUENTE_NORMAL,
            style="Custom.TCombobox"
        )
        self.combo_reportes["values"] = list(self._mapa_reportes().keys())
        self.combo_reportes.bind("<<ComboboxSelected>>", self._mostrar_campos_parametros)
        self.combo_reportes.pack(side="right", padx=10)
        self.combo_reportes.set("Seleccione un reporte...")
        
        # Separador visual
        ttk.Separator(panel, orient="horizontal").pack(fill="x", padx=20, pady=5)
        
        # Área de parámetros con fondo diferenciado
        self.frame_campos = tk.Frame(panel, bg=COLOR_PANEL, padx=10, pady=10)
        self.frame_campos.pack(fill="x", padx=15, pady=(5, 15))
        
        # Botones con mejor distribución
        botones = tk.Frame(panel, bg=COLOR_PANEL)
        botones.pack(pady=(0, 15))
        
        btn_style = {"bg": COLOR_PRIMARIO, "fg": COLOR_TEXTO, "font": FUENTE_BOTON,
                    "relief": tk.FLAT, "bd": 0, "padx": 15, "pady": 8}
        
        self._crear_boton(botones, "🔄 Generar", self.generar_reporte, **btn_style).pack(side="left", padx=5)
        self._crear_boton(botones, "🧹 Limpiar", self.limpiar_todo, **btn_style).pack(side="left", padx=5)
        self._crear_boton(botones, "📤 Exportar", self.exportar_pdf, **btn_style).pack(side="left", padx=5)
        
        # Tabla de resultados con mejor estilo
        self.tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        self.tabla_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Scrollbar personalizada
        self.scroll = ttk.Scrollbar(self.tabla_frame)
        self.scroll.pack(side="right", fill="y")
        
        # Configuración mejorada de la tabla
        self.tabla = ttk.Treeview(
            self.tabla_frame,
            show="headings",
            yscrollcommand=self.scroll.set,
            style="Custom.Treeview"
        )
        self.tabla.pack(fill="both", expand=True)
        self.scroll.config(command=self.tabla.yview)
        
        # Ajustar el padding de las celdas
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=25)

    def _crear_boton(self, master, texto, comando, **kwargs):
        default_style = {
            "bg": COLOR_PRIMARIO,
            "fg": COLOR_TEXTO,
            "font": FUENTE_BOTON,
            "relief": tk.FLAT,
            "bd": 0,
            "activebackground": COLOR_PRIMARIO_OSCURO,
            "activeforeground": COLOR_TEXTO,
            "cursor": "hand2",
            "padx": 12,
            "pady": 6
        }
        # Combinar estilos predeterminados con los personalizados
        btn_style = {**default_style, **kwargs}
        
        btn = tk.Button(master, text=texto, command=comando, **btn_style)
        
        # Efecto hover moderno
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=btn_style["bg"]))
        
        return btn

    def _mapa_reportes(self):
        return {
            "Total Ingresos del Mes": {"func": controlador_reporte.mostrar_total_ingresos_mes, "campos": []},
            "Total Gastos del Mes": {"func": controlador_reporte.mostrar_total_gasto_mes, "campos": []},
            "Total Facturas del Mes": {"func": controlador_reporte.mostrar_total_factura_mes, "campos": []},
            "Total Facturas por Estado": {"func": controlador_reporte.mostrar_total_factura_estado_mes, "campos": []},
            "Total Retiros del Mes": {"func": controlador_reporte.mostrar_total_retiros_mes, "campos": []},
            "Total Transacciones del Mes": {"func": controlador_reporte.mostrar_total_transacciones_mes, "campos": []},
            "Balance Total del Mes": {"func": controlador_reporte.mostrar_total_balance_mes, "campos": []},
            "Ganancia Neta": {"func": controlador_reporte.mostrar_ganancia_neta, "campos": ["fecha_inicio", "fecha_fin"]},
            "Salario por Empleado": {"func": controlador_reporte.mostrar_salario_empleado, "campos": ["empleado", "fecha_inicio", "fecha_fin"]},
        }


    def _mostrar_campos_parametros(self, event=None):
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.campos_dinamicos.clear()

        seleccion = self.combo_reportes.get()
        campos = self._mapa_reportes()[seleccion]["campos"]
        
        # Estilo común para etiquetas
        label_style = {"font": FUENTE_NORMAL, "bg": COLOR_PANEL, "fg": COLOR_TEXTO_SEC}
        
        row = 0
        if "empleado" in campos:
            tk.Label(self.frame_campos, text="Empleado:", **label_style).grid(
                row=row, column=0, padx=5, pady=5, sticky="e")
            self.filtro_empleado = self._crear_combo(self.frame_campos, controlador_empleado.mostrar_nombre_completo())
            self.filtro_empleado.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            self.campos_dinamicos["empleado"] = self.filtro_empleado
            row += 1

        if "fecha_inicio" in campos:
            tk.Label(self.frame_campos, text="Fecha Inicio:", **label_style).grid(
                row=row, column=0, padx=5, pady=5, sticky="e")
            desde = DateEntry(
                self.frame_campos, 
                date_pattern="yyyy-mm-dd", 
                font=FUENTE_NORMAL,
                background=COLOR_PRIMARIO,
                foreground=COLOR_TEXTO,
                bordercolor=COLOR_BORDE,
                headersbackground=COLOR_PANEL,
                normalbackground=COLOR_PANEL,
                normalforeground=COLOR_TEXTO,
                weekendbackground=COLOR_PANEL,
                weekendforeground=COLOR_TEXTO,
                selectbackground=COLOR_PRIMARIO_OSCURO
            )
            desde.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            self.campos_dinamicos["fecha_inicio"] = desde
            row += 1

        if "fecha_fin" in campos:
            tk.Label(self.frame_campos, text="Fecha Fin:", **label_style).grid(
                row=row, column=0, padx=5, pady=5, sticky="e")
            hasta = DateEntry(
                self.frame_campos, 
                date_pattern="yyyy-mm-dd", 
                font=FUENTE_NORMAL,
                background=COLOR_PRIMARIO,
                foreground=COLOR_TEXTO,
                bordercolor=COLOR_BORDE,
                headersbackground=COLOR_PANEL,
                normalbackground=COLOR_PANEL,
                normalforeground=COLOR_TEXTO,
                weekendbackground=COLOR_PANEL,
                weekendforeground=COLOR_TEXTO,
                selectbackground=COLOR_PRIMARIO_OSCURO
            )
            hasta.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            self.campos_dinamicos["fecha_fin"] = hasta

    def generar_reporte(self):
        # Mostrar feedback visual mientras se genera el reporte
        self.tabla.delete(*self.tabla.get_children())
        loading_label = tk.Label(self.tabla_frame, text="Generando reporte...", 
                            font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC)
        loading_label.pack(expand=True)
        self.update()
        
        try:
            seleccion = self.combo_reportes.get()
            if not seleccion:
                mensajes.mensajes_Error("Debe seleccionar un tipo de reporte.")
                return

            funcion = self._mapa_reportes()[seleccion]["func"]
            campos = self._mapa_reportes()[seleccion]["campos"]

            if not campos:
                datos = funcion()
            else:
                args = [self.campos_dinamicos[campo].get() for campo in campos]
                datos = funcion(*args)

            loading_label.destroy()

            # Normalizar datos a listas de tuplas
            if isinstance(datos, (int, float, str)):
                datos = [(datos,)]
            elif isinstance(datos, dict):
                datos = [tuple(datos.values())]
            elif isinstance(datos, list) and all(not isinstance(item, (list, tuple)) for item in datos):
                datos = [(item,) for item in datos]

            self.resultados = datos

            if seleccion == "Salario por Empleado":
                encabezados = ["ID", "Empleado", "Desde", "Hasta", "Total Salarios"]

            elif seleccion == "Ganancia Neta":
                encabezados = ["Desde", "Hasta", "Total Retiros", "Total Gastos", "Ganancia Neta"]


            elif seleccion == "Total Ingresos del Mes":
                encabezados = [
                    "Cantidad Ingresos",
                    "Total Ingresos del Mes",
                    "Promedio Ingreso",
                    "Desde Fecha",
                    "Hasta Fecha"
                ]

            elif seleccion == "Total Gastos del Mes":
                encabezados = [
                    "Cantidad Gastos",
                    "Total Gastos del Mes",
                    "Promedio Gasto",
                    "Desde Fecha",
                    "Hasta Fecha"
                ]

            elif seleccion == "Total Retiros del Mes":
                encabezados = [
                    "Cantidad Retiros",
                    "Total Retiros del Mes",
                    "Promedio Retiro",
                    "Desde Fecha",
                    "Hasta Fecha"
                ]

            elif seleccion == "Total Transacciones del Mes":
                encabezados = [
                    "Cantidad Transacciones",
                    "Total Transacciones del Mes",
                    "Promedio Transacción",
                    "Desde Fecha",
                    "Hasta Fecha"
                ]

            elif seleccion == "Balance Total del Mes":
                encabezados = [
                    "Balance Neto Mes",
                    "Total Ingresos",
                    "Total Gastos",
                    "Total Retiros",
                    "Total Transacciones",
                    "Desde Fecha",
                    "Hasta Fecha"
                ]

            elif seleccion == "Total Facturas del Mes":
                encabezados = [
                    "Cantidad Facturas",
                    "Monto Total Facturado",
                    "Monto Promedio Factura",
                    "Desde Fecha",
                    "Hasta Fecha"
                ]

            elif seleccion == "Total Facturas por Estado":
                encabezados = [
                    "Estado",
                    "Cantidad",
                    "Monto Total",
                    "Monto Promedio",
                    "Desde Fecha",
                    "Hasta Fecha"
                ]

            else:
                if datos and isinstance(datos[0], (list, tuple)):
                    encabezados = [f"Columna {i+1}" for i in range(len(datos[0]))]
                else:
                    encabezados = ["Resultado"]

            # ✅ Configuración común de la tabla después de definir encabezados
            self.tabla["columns"] = encabezados
            self.tabla["show"] = "headings"

            for col in encabezados:
                self.tabla.heading(col, text=col)
                self.tabla.column(col, anchor="center")  # <-- aquí se centra el contenido




            self._cargar_tabla(datos, encabezados)

        except Exception as e:
            loading_label.destroy()
            mensajes.mensajes_Error(f"Error al generar reporte: {str(e)}")

    def _cargar_tabla(self, datos, nombres_columnas=None):
        self.tabla.delete(*self.tabla.get_children())

        if not datos:
            self.tabla["columns"] = []
            return

        if nombres_columnas is None:
            columnas = list(range(len(datos[0])))
            nombres_columnas = [f"Columna {i+1}" for i in columnas]
        else:
            columnas = list(range(len(nombres_columnas)))

        self.tabla["columns"] = columnas

        for i, col in enumerate(columnas):
            self.tabla.heading(col, text=nombres_columnas[i])
            self.tabla.column(col, width=150, anchor="w")

        for fila in datos:
            self.tabla.insert("", "end", values=fila if isinstance(fila, (list, tuple)) else [fila])


    def exportar_pdf(self):
        if not self.resultados:
            mensajes.mensajes_Error("No hay datos para exportar.")
            return

        columnas = [self.tabla.heading(col)["text"] for col in self.tabla["columns"]]
        exportar_pdf(self.resultados, columnas, titulo=self.combo_reportes.get())

    def limpiar_todo(self):
        self.combo_reportes.set("")
        self.resultados = []
        
        # Limpiar campos visuales
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.campos_dinamicos.clear()
        
        # Limpiar tabla
        self._cargar_tabla([])
