# ventana_planilla.py
import tkinter as tk
from tkinter import ttk
from controllers import controlador_planilla, controlador_empleado
from tkcalendar import DateEntry
from datetime import datetime

# Estilos compartidos
COLOR_FONDO = "#1B1F2A"
COLOR_PANEL = "#252B3A"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_SEC = "#B0B4C8"
COLOR_PRIMARIO = "#2ECC71"
COLOR_PRIMARIO_OSCURO = "#27AE60"
COLOR_HOVER = "#34D178"
COLOR_ACCION = "#4CAF50"
COLOR_BORDE = "#34495E"
COLOR_ERROR = "#E74C3C"

FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 14)
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")

class VentanaPlanilla(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_planilla
        self.pack(fill="both", expand=True)  # ⬅ Hacemos que la clase se adapte
        self.controlador_empleado = controlador_empleado
        self.id_seleccionado = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._configurar_estilos()
        self._construir_ui()
        self.cargar_planillas()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Configurar Treeview
        estilo.configure("Treeview", 
                        background=COLOR_PANEL, 
                        foreground=COLOR_TEXTO,
                        fieldbackground=COLOR_PANEL, 
                        font=FUENTE_NORMAL,
                        rowheight=25,
                        bordercolor=COLOR_BORDE)
        
        estilo.configure("Treeview.Heading", 
                        background=COLOR_BORDE, 
                        foreground=COLOR_TEXTO,
                        font=FUENTE_BOTON,
                        relief="flat")
        
        estilo.map("Treeview", 
                 background=[("selected", COLOR_PRIMARIO_OSCURO)],
                 foreground=[("selected", COLOR_TEXTO)])

        # Configurar Spinbox
        estilo.configure("TSpinbox",
                        fieldbackground=COLOR_PANEL,
                        background=COLOR_PANEL,
                        foreground=COLOR_TEXTO,
                        bordercolor=COLOR_BORDE,
                        lightcolor=COLOR_PRIMARIO,
                        darkcolor=COLOR_PRIMARIO_OSCURO,
                        arrowsize=12)
        
        # Configurar Botones
        estilo.configure("Accent.TButton",
                        background=COLOR_PRIMARIO,
                        foreground=COLOR_TEXTO,
                        font=FUENTE_BOTON,
                        bordercolor=COLOR_PRIMARIO_OSCURO,
                        focusthickness=3,
                        focuscolor=COLOR_PRIMARIO_OSCURO)
        
        estilo.map("Accent.TButton",
                  background=[("active", COLOR_HOVER), ("!disabled", COLOR_PRIMARIO)],
                  foreground=[("!disabled", COLOR_TEXTO)])

    def _crear_combo(self, master, datos):
        nombres = [d[1] if isinstance(d, (list, tuple)) else d for d in datos] if datos else []
        estado = "readonly" if nombres else "disabled"

        combo = ttk.Combobox(master, values=nombres, state=estado, width=37, style="TCombobox")
        combo.set(nombres[0] if nombres else "Seleccione empleado")
        return combo

    def _crear_boton(self, master, texto, comando, estilo="Accent.TButton"):
        btn = ttk.Button(master, text=texto, style=estilo, command=comando)
        return btn

    def _crear_spinbox(self, master, from_, to, increment, width=15):
        return ttk.Spinbox(master, from_=from_, to=to, increment=increment, 
                          font=FUENTE_NORMAL, width=width, style="TSpinbox")

    def _construir_ui(self):
        main_container = tk.Frame(self, bg=COLOR_FONDO)
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        main_container.grid_rowconfigure(2, weight=1)  # La tabla se expande
        main_container.grid_columnconfigure(0, weight=1)

        # ======= FORMULARIO =======
        form_panel = tk.Frame(main_container, bg=COLOR_PANEL, bd=2, relief=tk.GROOVE,
                            highlightbackground=COLOR_BORDE, highlightthickness=1)
        form_panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        form_panel.grid_columnconfigure(1, weight=1)
        form_panel.grid_columnconfigure(3, weight=1)
        form_panel.grid_columnconfigure(5, weight=1)

        # Cabecera
        tk.Label(form_panel, text="Gestión de Planillas", font=FUENTE_TITULO,
                bg=COLOR_PANEL, fg=COLOR_PRIMARIO).grid(row=0, column=0, columnspan=6, sticky="w", pady=10, padx=10)

        # ===== Fila 1 =====
        tk.Label(form_panel, text="Empleado:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w", pady=5, padx=10)
        empleados = self.controlador_empleado.mostrar_nombre_completo()
        self.combo_empleado = self._crear_combo(form_panel, empleados)
        self.combo_empleado.config(width=25)
        self.combo_empleado.grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(form_panel, text="Fecha Inicio:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=2, sticky="w", pady=5)
        self.fecha_inicio = DateEntry(form_panel, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd', width=12)
        self.fecha_inicio.grid(row=1, column=3, pady=5, sticky="w")

        tk.Label(form_panel, text="Fecha Fin:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=4, sticky="w", pady=5)
        self.fecha_fin = DateEntry(form_panel, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd', width=12)
        self.fecha_fin.grid(row=1, column=5, pady=5, sticky="w")

        # ===== Fila 2 =====
        tk.Label(form_panel, text="Horas Trabajadas:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.entry_horas = self._crear_spinbox(form_panel, 0, 500, 1, 8)
        self.entry_horas.grid(row=2, column=1, pady=5, sticky="w")
        self.entry_horas.bind("<KeyRelease>", self._calcular_salario)

        tk.Label(form_panel, text="Pago por Hora ($):", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=2, column=2, sticky="w", pady=5)
        self.entry_pago = self._crear_spinbox(form_panel, 0, 1000, 0.5, 8)
        self.entry_pago.grid(row=2, column=3, pady=5, sticky="w")
        self.entry_pago.bind("<KeyRelease>", self._calcular_salario)

        tk.Label(form_panel, text="Salario Total ($):", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=2, column=4, sticky="w", pady=5)
        self.entry_salario = self._crear_spinbox(form_panel, 0, 1000000, 100, 10)
        self.entry_salario.grid(row=2, column=5, pady=5, sticky="w")

        # Comentarios
        tk.Label(form_panel, text="Comentarios:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=3, column=0, sticky="nw", pady=5, padx=10)
        self.entry_comentario = tk.Text(form_panel, font=FUENTE_NORMAL, height=3,
                                        bg=COLOR_PANEL, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                        highlightbackground=COLOR_BORDE, highlightthickness=1, width=60)
        self.entry_comentario.grid(row=3, column=1, columnspan=5, pady=5, sticky="ew")

        # ======= FILTROS =======
        filters_panel = tk.Frame(main_container, bg=COLOR_PANEL, bd=2, relief=tk.GROOVE,
                                highlightbackground=COLOR_BORDE, highlightthickness=1)
        filters_panel.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        filters_panel.grid_columnconfigure(1, weight=1)
        filters_panel.grid_columnconfigure(3, weight=1)

        tk.Label(filters_panel, text="Filtros", font=FUENTE_SUBTITULO,
                bg=COLOR_PANEL, fg=COLOR_PRIMARIO).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=5)

        tk.Label(filters_panel, text="Fecha Inicio:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.filtro_fecha_inicio = DateEntry(filters_panel, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd', width=12)
        self.filtro_fecha_inicio.grid(row=1, column=1, pady=5, sticky="w")

        tk.Label(filters_panel, text="Fecha Fin:", font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=2, sticky="w", pady=5)
        self.filtro_fecha_fin = DateEntry(filters_panel, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd', width=12)
        self.filtro_fecha_fin.grid(row=1, column=3, pady=5, sticky="w")

        self.btn_filtrar = self._crear_boton(filters_panel, "Filtrar", self.filtrar_planillas)
        self.btn_filtrar.grid(row=1, column=4, padx=10, pady=5)

        # ======= TABLA =======
        table_panel = tk.Frame(main_container, bg=COLOR_PANEL, bd=2, relief=tk.GROOVE,
                            highlightbackground=COLOR_BORDE, highlightthickness=1)
        table_panel.grid(row=2, column=0, sticky="nsew")

        table_container = tk.Frame(table_panel, bg=COLOR_PANEL)
        table_container.pack(fill="both", expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(table_container, orient="vertical")
        scroll_x = ttk.Scrollbar(table_container, orient="horizontal")

        columnas = ("id", "empleado", "inicio", "fin", "horas", "pago_hora", "salario", "comentario")
        self.tabla = ttk.Treeview(table_container, columns=columnas, show="headings",
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Config columnas más compactas
        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("empleado", width=150, anchor="w")
        self.tabla.column("inicio", width=90, anchor="center")
        self.tabla.column("fin", width=90, anchor="center")
        self.tabla.column("horas", width=70, anchor="center")
        self.tabla.column("pago_hora", width=90, anchor="e")
        self.tabla.column("salario", width=100, anchor="e")
        self.tabla.column("comentario", width=200, anchor="w")

        for col in columnas:
            self.tabla.heading(col, text=col.replace("_", " ").title())

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # ======= BOTONES =======
        btn_frame = tk.Frame(main_container, bg=COLOR_FONDO)
        btn_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        self.total_label = tk.Label(btn_frame, text="Total Gastos: ₡0.00",
                                    bg=COLOR_PANEL, fg=COLOR_TEXTO,
                                    font=("Segoe UI", 12, "bold"))
        self.total_label.pack(side="right", pady=5, padx=10)

        self.btn_guardar = self._crear_boton(btn_frame, "Guardar", self.guardar)
        self.btn_guardar.pack(side="left", padx=5)

        self.btn_actualizar = self._crear_boton(btn_frame, "Actualizar", self.actualizar)
        self.btn_actualizar.pack(side="left", padx=5)

        self.btn_eliminar = self._crear_boton(btn_frame, "Eliminar", self.eliminar)
        self.btn_eliminar.pack(side="left", padx=5)

        self.btn_limpiar = self._crear_boton(btn_frame, "Limpiar", self.limpiar)
        self.btn_limpiar.pack(side="left", padx=5)






    def _calcular_salario(self, event=None):
        try:
            horas = float(self.entry_horas.get())
            pago = float(self.entry_pago.get())
            salario = horas * pago
            self.entry_salario.delete(0, tk.END)
            self.entry_salario.insert(0, f"{salario:.2f}")
        except ValueError:
            self.entry_salario.delete(0, tk.END)
            self.entry_salario.insert(0, "0.00")

    def _validar_datos(self):
        errores = []
        if not self.combo_empleado.get():
            errores.append("Debe seleccionar un empleado.")
        if self.fecha_fin.get_date() < self.fecha_inicio.get_date():
            errores.append("La fecha fin no puede ser anterior a la fecha inicio.")
        try:
            horas = float(self.entry_horas.get())
            if horas < 0:
                errores.append("Horas trabajadas no puede ser negativo.")
        except ValueError:
            errores.append("Horas trabajadas debe ser un número válido.")
        try:
            pago = float(self.entry_pago.get())
            if pago < 0:
                errores.append("Pago por hora no puede ser negativo.")
        except ValueError:
            errores.append("Pago por hora debe ser un número válido.")
        return errores



    def cargar_planillas(self):
        self.tabla.delete(*self.tabla.get_children())
        datos = self.model.mostrar_planilla()
        if isinstance(datos, list):
            for fila in datos:
                # Reordenar los campos para que coincidan con los definidos en el Treeview
                fila_reordenada = (
                    fila[0],  # planilla_id
                    fila[7],  # empleado_nombre (originalmente al final)
                    fila[1],  # fecha_inicio
                    fila[2],  # fecha_fin
                    fila[3] if fila[3] is not None else 0,  # horas_trabajadas
                    fila[4] if fila[4] is not None else 0.00,  # pago_por_hora
                    fila[5],  # salario
                    fila[6]   # comentarios
                )
                self.tabla.insert("", "end", values=fila_reordenada)
            
        self.actualizar_total_planilla()




    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = valores[0]
            self.combo_empleado.set(valores[1])
            self.fecha_inicio.set_date(valores[2])
            self.fecha_fin.set_date(valores[3])
            self.entry_horas.delete(0, tk.END)
            self.entry_horas.insert(0, valores[4])
            self.entry_pago.delete(0, tk.END)
            self.entry_pago.insert(0, valores[5])
            self.entry_salario.delete(0, tk.END)
            self.entry_salario.insert(0, valores[6])
            self.entry_comentario.delete("1.0", tk.END)
            self.entry_comentario.insert("1.0", valores[7] if len(valores) > 7 else "")
            



    def calcular_total_salarios(self):
        total = 0.0
        for item in self.tabla.get_children():
            salario = self.tabla.item(item, "values")[6]
            try:
                total += float(salario)
            except (TypeError, ValueError):
                continue

        from utils.mensajes import mensajes
        mensajes.mensajes_informacion(f"Total de salarios: ${total:,.2f}")


    def limpiar(self):
        self.id_seleccionado = None
        self.combo_empleado.set("")
        self.fecha_inicio.set_date(datetime.now())
        self.fecha_fin.set_date(datetime.now())
        self.entry_horas.delete(0, tk.END)
        self.entry_pago.delete(0, tk.END)
        self.entry_salario.delete(0, tk.END)
        self.entry_comentario.delete("1.0", tk.END)
        self.cargar_planillas()

    def guardar(self):
        self.model.guardar_planilla(
            self.combo_empleado.get(),
            self.fecha_inicio.get_date(),
            self.fecha_fin.get_date(),
            float(self.entry_horas.get() or 0),
            float(self.entry_pago.get() or 0),
            float(self.entry_salario.get() or 0),
            self.entry_comentario.get("1.0", tk.END).strip()
        )
        self.limpiar()

    def actualizar(self):


        self.model.actualizar_planilla(
            self.id_seleccionado,
            self.combo_empleado.get(),
            self.fecha_inicio.get_date(),
            self.fecha_fin.get_date(),
            float(self.entry_horas.get() or 0),
            float(self.entry_pago.get() or 0),
            float(self.entry_salario.get() or 0),
            self.entry_comentario.get("1.0", tk.END).strip()
        )
        self.limpiar()


    def eliminar(self):    
        self.model.eliminar_planilla(self.id_seleccionado)
        self.limpiar()

    def filtrar_planillas(self):
        # Obtener fechas de los campos
        fecha_inicio = self.filtro_fecha_inicio.get()
        fecha_fin = self.filtro_fecha_fin.get()  # ← aquí tenías un error, era función sin paréntesis

        # Llamar al controlador para filtrar los datos
        resultados = controlador_planilla.filtrar_planilla(fecha_inicio, fecha_fin)

        # Limpiar la tabla
        self.tabla.delete(*self.tabla.get_children())

        # Mostrar los resultados
        if isinstance(resultados, list):
            for fila in resultados:
                fila_reordenada = (
                    fila[0],  # planilla_id
                    fila[7],  # empleado_nombre
                    fila[1],  # fecha_inicio
                    fila[2],  # fecha_fin
                    fila[3] if fila[3] is not None else 0,
                    fila[4] if fila[4] is not None else 0.00,
                    fila[5],  # salario
                    fila[6]   # comentarios
                )
                self.tabla.insert("", "end", values=fila_reordenada)
        
        self.actualizar_total_planilla()



        
    def actualizar_total_planilla(self):
        total = 0
        for child in self.tabla.get_children():
            monto_str = self.tabla.item(child)["values"][6]  # columna monto
            try:
                monto = float(monto_str)
                total += monto
            except (ValueError, TypeError):
                pass

        self.total_label.config(text=f"Total Planilla: ₡{total:,.2f}")
