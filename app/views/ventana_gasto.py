import tkinter as tk
from tkinter import Canvas, ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import date
import os
import tempfile

from controllers import controlador_gasto, controlador_empleado, controlador_metodo_pago, controlador_banco

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
COLOR_BOTON = COLOR_PRIMARIO     # Color para botones principales
COLOR_BOTON_SEC = "#3498db"      # Color para botones secundarios

# Fuentes actualizadas
FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 14)
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")
FUENTE_MENU = ("Segoe UI", 11)

class VentanaGasto(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_gasto
        self.id_seleccionado = None
        self.documento_blob = None
        self.documentos_en_memoria = {}
        self.nombre_documento = ""

        self._construir_ui()
        self.cargar_gastos()


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


    def _crear_boton(self, master, texto, comando, color=COLOR_BOTON):
        btn = tk.Button(master, text=texto, font=FUENTE_BOTON, bg=color, fg=COLOR_TEXTO,
                       activebackground=COLOR_HOVER, activeforeground=COLOR_TEXTO,
                       relief=tk.FLAT, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

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

        # Título
        tk.Label(panel, text="Gestión de Gastos", font=FUENTE_TITULO, 
                bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(pady=10)
        
        # Filtros
        filtros_frame = tk.Frame(panel, bg=COLOR_PANEL)
        filtros_frame.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(filtros_frame, text="Desde:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5)
        self.filtro_fecha_inicio = DateEntry(filtros_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd',
                                            background=COLOR_PANEL, foreground=COLOR_TEXTO)
        self.filtro_fecha_inicio.grid(row=0, column=1, padx=5)

        tk.Label(filtros_frame, text="Hasta:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=0, column=2, padx=5)
        self.filtro_fecha_fin = DateEntry(filtros_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd',
                                        background=COLOR_PANEL, foreground=COLOR_TEXTO)
        self.filtro_fecha_fin.grid(row=0, column=3, padx=5)

        tk.Label(filtros_frame, text="Empleado:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=0, column=4, padx=5)
        self.filtro_empleado = self._crear_combo(filtros_frame, controlador_empleado.mostrar_nombre_completo())
        self.filtro_empleado.grid(row=0, column=5, padx=5)

        btn_filtrar = self._crear_boton(filtros_frame, "Filtrar", self.aplicar_filtro, COLOR_BOTON_SEC)
        btn_filtrar.grid(row=0, column=6, padx=10)


        # Formulario
        form = tk.Frame(panel, bg=COLOR_PANEL)
        form.pack(fill="x", padx=20, pady=10)

        # Configurar el grid
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        # Fila 1
        tk.Label(form, text="Fecha:", font=FUENTE_NORMAL, 
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w", pady=5)
        self.fecha = DateEntry(form, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd',
                             background=COLOR_PANEL, foreground=COLOR_TEXTO)
        self.fecha.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(form, text="Monto:", font=FUENTE_NORMAL, 
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=0, column=2, sticky="w", pady=5)
        self.entry_monto = tk.Entry(form, font=FUENTE_NORMAL, bg=COLOR_PANEL, 
                                   fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
        self.entry_monto.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        # Fila 2
        tk.Label(form, text="Método Pago:", font=FUENTE_NORMAL, 
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w", pady=5)
        self.combo_metodo = self._crear_combo(form, controlador_metodo_pago.mostrar_metodos_pago())
        self.combo_metodo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(form, text="Empleado:", font=FUENTE_NORMAL, 
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=1, column=2, sticky="w", pady=5)
        self.combo_empleado = self._crear_combo(form, controlador_empleado.mostrar_nombre_completo())
        self.combo_empleado.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        # Fila 3
        tk.Label(form, text="Banco:", font=FUENTE_NORMAL, 
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="w", pady=5)
        self.combo_banco = self._crear_combo(form, [""] + controlador_banco.traer_cuenta_iban())
        self.combo_banco.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(form, text="Descripción:", font=FUENTE_NORMAL, 
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=2, column=2, sticky="w", pady=5)
        self.entry_desc = tk.Entry(form, font=FUENTE_NORMAL, bg=COLOR_PANEL, 
                                  fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
        self.entry_desc.grid(row=2, column=3, sticky="ew", padx=5, pady=5)

        # Fila 4: Documento
        tk.Label(form, text="Documento:", font=FUENTE_NORMAL, 
                bg=COLOR_PANEL, fg=COLOR_TEXTO).grid(row=3, column=0, sticky="w", pady=5)
        
        self.btn_documento = self._crear_boton(form, "Seleccionar Documento", 
                                            self.seleccionar_documento, COLOR_BOTON_SEC)
        self.btn_documento.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        self.lbl_documento = tk.Label(form, text="Ningún documento seleccionado", 
                                     font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO_SEC)
        self.lbl_documento.grid(row=3, column=2, sticky="w", padx=5, pady=5)
        
        self.btn_abrir_documento = self._crear_boton(form, "Abrir Documento", 
                                                   self.abrir_documento, COLOR_BOTON_SEC)
        self.btn_abrir_documento.grid(row=3, column=3, sticky="ew", padx=5, pady=5)
        self.btn_abrir_documento.grid_remove()

        # Tabla
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Configurar estilo para la tabla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                       background=COLOR_PANEL,
                       foreground=COLOR_TEXTO,
                       fieldbackground=COLOR_PANEL,
                       borderwidth=0,
                       font=FUENTE_NORMAL)
        style.configure("Treeview.Heading", 
                       background=COLOR_PRIMARIO_OSCURO,
                       foreground=COLOR_TEXTO,
                       font=FUENTE_BOTON,
                       relief=tk.FLAT)
        style.map("Treeview", 
                 background=[('selected', COLOR_BOTON_SEC)],
                 foreground=[('selected', COLOR_TEXTO)])
        
        columnas = ("id", "fecha", "monto", "metodo", "banco", "empleado", "descripcion", "abrir")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=100 if col != "abrir" else 80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.pack(fill="both", expand=True)
        
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        self.tabla.bind("<Double-1>", self._click_en_abrir)

        # Total gastos
        self.total_label = tk.Label(panel, text="Total Gastos: ₡0.00", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        self.total_label.pack(pady=(5, 10), anchor="e", padx=20)

        # Botones
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=10)
        
        botones = [
            ("Guardar", self.guardar, COLOR_PRIMARIO),
            ("Actualizar", self.actualizar, COLOR_BOTON_SEC),
            ("Eliminar", self.eliminar, "#e74c3c"),
            ("Limpiar", self.limpiar, COLOR_TEXTO_SEC)
        ]
        
        for texto, accion, color in botones:
            btn = self._crear_boton(btn_frame, texto, accion, color)
            btn.pack(side="left", padx=10, ipadx=10, ipady=5)

    def seleccionar_documento(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos", "*.pdf *.jpg *.png *.jpeg")])
        if ruta:
            with open(ruta, "rb") as f:
                self.documento_blob = f.read()
            self.nombre_documento = os.path.basename(ruta)
            self.lbl_documento.config(text=self.nombre_documento, fg=COLOR_PRIMARIO)
            self.btn_abrir_documento.grid()

    def abrir_documento(self):
        if self.documento_blob:
            try:
                # Determinar la extensión del archivo
                if self.documento_blob[:4] == b"%PDF":
                    ext = ".pdf"
                elif self.documento_blob[:8] == b"\x89PNG\r\n\x1a\n":
                    ext = ".png"
                elif self.documento_blob[:2] == b"\xff\xd8":
                    ext = ".jpg"
                else:
                    ext = ".bin"
                
                # Crear archivo temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp:
                    temp.write(self.documento_blob)
                    temp_path = temp.name
                
                # Abrir el archivo
                os.startfile(temp_path)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el documento: {str(e)}")


    def guardar(self):
        self.model.guardar_gasto(
            self.fecha.get(),
            self.entry_monto.get(),
            self.combo_metodo.get(),
            self.entry_desc.get(),
            self.documento_blob,
            self.combo_empleado.get(),
            self.combo_banco.get()
            )
        self.limpiar()

    def actualizar(self):
        valor_banco = self.combo_banco.get()
        if valor_banco == "Sin cuenta": 
            valor_banco = None

        self.model.actualizar_gasto(
            self.id_seleccionado,
            self.fecha.get(),
            self.entry_monto.get(),
            self.combo_metodo.get(),
            self.entry_desc.get(),
            self.documento_blob,
            self.combo_empleado.get(),
            valor_banco
        )
        self.limpiar()

    def eliminar(self):
        self.model.eliminar_gasto(self.id_seleccionado)
        self.limpiar()


    def limpiar(self):
        self.id_seleccionado = None
        self.fecha.set_date(date.today())
        self.entry_monto.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.combo_metodo.current(0)
        self.combo_empleado.current(0)
        self.combo_banco.current(0)
        self.documento_blob = None
        self.nombre_documento = ""
        self.lbl_documento.config(text="Ningún documento seleccionado", fg=COLOR_TEXTO_SEC)
        self.btn_abrir_documento.grid_remove()
        self.cargar_gastos()

    def cargar_gastos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.documentos_en_memoria.clear()
        datos = self.model.mostrar_gasto()
        if isinstance(datos, list):
            for fila in datos:
                gasto_id = fila[0]
                fecha = fila[1]
                monto = fila[2]
                metodo = fila[4]
                empleado = fila[5]
                banco = fila[6] if fila[6] else ""
                descripcion = fila[3]
                documento_blob = fila[7]  # binario
                
                self.documentos_en_memoria[gasto_id] = documento_blob
                self.tabla.insert("", "end", values=(
                    gasto_id, 
                    fecha, 
                    monto, 
                    metodo, 
                    empleado, 
                    banco, 
                    descripcion, 
                    "Abrir" if documento_blob else ""
                ))
        self.actualizar_total_gasto()

    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = valores[0]
            self.fecha.set_date(valores[1])
            self.entry_monto.delete(0, tk.END)
            self.entry_monto.insert(0, valores[2])
            self.combo_metodo.set(valores[3])
            self.combo_empleado.set(valores[5])
            self.combo_banco.set(valores[4] if valores[4] else "")
            self.entry_desc.delete(0, tk.END)
            self.entry_desc.insert(0, valores[6])
            
            self.documento_blob = self.documentos_en_memoria.get(int(self.id_seleccionado))
            if self.documento_blob:
                self.lbl_documento.config(text=f"Documento #{self.id_seleccionado}", fg=COLOR_PRIMARIO)
                self.btn_abrir_documento.grid()
            else:
                self.lbl_documento.config(text="Sin documento", fg=COLOR_TEXTO_SEC)
                self.btn_abrir_documento.grid_remove()

    def _click_en_abrir(self, event):
        region = self.tabla.identify("region", event.x, event.y)
        if region == "cell":
            fila = self.tabla.identify_row(event.y)
            col = self.tabla.identify_column(event.x)
            if col == "#8":
                item = self.tabla.item(fila)
                id_fila = item["values"][0]
                documento = self.documentos_en_memoria.get(int(id_fila))
                if documento:
                    self.documento_blob = documento
                    self.abrir_documento()
    

    def aplicar_filtro(self):
        fecha_inicio = self.filtro_fecha_inicio.get_date() if self.filtro_fecha_inicio.get() else None
        fecha_fin = self.filtro_fecha_fin.get_date() if self.filtro_fecha_fin.get() else None
        empleado = self.filtro_empleado.get()

        # El combo puede tener "Sin opciones", validamos eso
        if empleado == "Sin opciones":
            empleado = None

        resultados = self.model.filtrar_gasto_fecha_empleado(
            fecha_inicio.strftime("%Y-%m-%d") if fecha_inicio else None,
            fecha_fin.strftime("%Y-%m-%d") if fecha_fin else None,
            empleado
        )

        self._mostrar_resultados_en_tabla(resultados)
        self.actualizar_total_gasto()


    def _mostrar_resultados_en_tabla(self, datos):
        self.tabla.delete(*self.tabla.get_children())
        self.documentos_en_memoria.clear()
        
        if isinstance(datos, list):
            for fila in datos:
                gasto_id = fila[0]
                fecha = fila[1]
                monto = fila[2]
                metodo = fila[4]
                empleado = fila[5]
                banco = fila[6] if fila[6] else ""
                descripcion = fila[3]
                documento_blob = fila[7]
                
                self.documentos_en_memoria[gasto_id] = documento_blob
                self.tabla.insert("", "end", values=(
                    gasto_id, fecha, monto, metodo, empleado, banco, descripcion,
                    "Abrir" if documento_blob else ""
                ))


        
    def actualizar_total_gasto(self):
        total = 0
        for child in self.tabla.get_children():
            monto_str = self.tabla.item(child)["values"][2]  # columna monto
            try:
                monto = float(monto_str)
                total += monto
            except (ValueError, TypeError):
                pass

        self.total_label.config(text=f"Total Gastos: ₡{total:,.2f}")
