import tkinter as tk
from tkinter import Canvas, ttk, filedialog
from tkcalendar import DateEntry
from datetime import date
import os

from controllers import controlador_factura, controlador_cliente
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

class VentanaFactura(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_factura
        self.id_seleccionado = None
        self.documento_pdf = None
        self.documentos_en_memoria = {}

        self._configurar_estilos()
        self._construir_ui()
        self.cargar_facturas()


    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, borderwidth=0, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", background=COLOR_BORDE, foreground=COLOR_TEXTO,
                         font=FUENTE_BOTON, relief="flat")
        estilo.map("Treeview", background=[("selected", COLOR_PRIMARIO_OSCURO)],
                   foreground=[("selected", COLOR_TEXTO)])

    def _crear_combo(self, master, datos):
        nombres = [d for d in datos] if datos else []
        combo = ttk.Combobox(master, values=nombres, state="readonly", width=37)
        if nombres:
            combo.current(0)
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
        cabecera.pack(fill="x", pady=10, padx=20)
        tk.Label(cabecera, text="Gestión de Facturas", font=FUENTE_TITULO,
                 bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")

        filtro_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        filtro_frame.pack(side="right")

        # Fila 1: filtro por fechas y botón
        fechas_frame = tk.Frame(filtro_frame, bg=COLOR_PANEL)
        fechas_frame.pack(fill="x", pady=(0, 10))

        tk.Label(fechas_frame, text="Desde:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_fecha_inicio = DateEntry(fechas_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.filtro_fecha_inicio.pack(side="left", padx=(0, 10))

        tk.Label(fechas_frame, text="Hasta:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_fecha_fin = DateEntry(fechas_frame, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.filtro_fecha_fin.pack(side="left", padx=(0, 10))

        btn_filtro = tk.Button(fechas_frame, text="Filtrar", bg=COLOR_ACCION, fg=COLOR_TEXTO,
                            font=FUENTE_BOTON, relief=tk.FLAT,
                            activebackground=COLOR_PRIMARIO_OSCURO,
                            activeforeground=COLOR_TEXTO,
                            command=self.aplicar_filtro)
        btn_filtro.pack(side="left")
        btn_filtro.bind("<Enter>", lambda e: btn_filtro.config(bg=COLOR_HOVER))
        btn_filtro.bind("<Leave>", lambda e: btn_filtro.config(bg=COLOR_ACCION))


        # Fila 2: filtro por cliente y pagada y botón
        cliente_frame = tk.Frame(filtro_frame, bg=COLOR_PANEL)
        cliente_frame.pack(fill="x")

        tk.Label(cliente_frame, text="Cliente:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_cliente = self._crear_combo(cliente_frame, [p[1] for p in controlador_cliente.mostrar_clientes()])
        self.filtro_cliente.set("")  # Para permitir selección vacía
        self.filtro_cliente.pack(side="left", padx=(0, 10))

        tk.Label(cliente_frame, text="Pagada:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        self.filtro_pagada = ttk.Combobox(cliente_frame, values=["Sí", "No"], state="readonly", width=5)
        self.filtro_pagada.set("")  # Sin selección por defecto
        self.filtro_pagada.pack(side="left", padx=(0, 10))

        btn_filtro_nombre_pagada = tk.Button(cliente_frame, text="Filtrar por Cliente y Pago", bg=COLOR_ACCION, fg=COLOR_TEXTO,
                                            font=FUENTE_BOTON, relief=tk.FLAT,
                                            activebackground=COLOR_PRIMARIO_OSCURO,
                                            activeforeground=COLOR_TEXTO,
                                            command=self.aplicar_filtro_nombre_pagada)
        btn_filtro_nombre_pagada.pack(side="left", padx=(5, 0))
        btn_filtro_nombre_pagada.bind("<Enter>", lambda e: btn_filtro_nombre_pagada.config(bg=COLOR_HOVER))
        btn_filtro_nombre_pagada.bind("<Leave>", lambda e: btn_filtro_nombre_pagada.config(bg=COLOR_ACCION))


        # Formulario
        form = tk.Frame(panel, bg=COLOR_PANEL)
        form.pack(fill="x", padx=20, pady=10)

        # Fila 0
        tk.Label(form, text="Cliente:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        clientes = [p[1] for p in controlador_cliente.mostrar_clientes()]
        self.combo_cliente = self._crear_combo(form, clientes)
        self.combo_cliente.grid(row=0, column=1, pady=6, sticky="ew")

        tk.Label(form, text="Número Factura:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=2, sticky="w", padx=(10, 10))
        self.entry_numero = tk.Entry(form, font=FUENTE_NORMAL)
        self.entry_numero.grid(row=0, column=3, pady=6, sticky="ew")

        # Fila 1
        tk.Label(form, text="Fecha:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        self.fecha = DateEntry(form, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.fecha.grid(row=1, column=1, pady=6, sticky="ew")

        tk.Label(form, text="Monto:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=2, sticky="w", padx=(10, 10))
        self.entry_monto = tk.Entry(form, font=FUENTE_NORMAL)
        self.entry_monto.grid(row=1, column=3, pady=6, sticky="ew")


        # Fila 2 (ajustada hacia la izquierda)
        tk.Label(form, text="Documento:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=2, column=0, sticky="e", pady=6)  # de 1 a 0

        self.btn_documento = tk.Button(form, text="Seleccionar Documento", font=FUENTE_NORMAL,
                                    bg=COLOR_ACCION, fg=COLOR_TEXTO, command=self.seleccionar_documento)
        self.btn_documento.grid(row=2, column=1, pady=6, sticky="ew")  # de 2 a 1

        self.btn_abrir_documento = tk.Button(form, text="Abrir Documento", font=FUENTE_NORMAL,
                                            bg=COLOR_ACCION, fg=COLOR_TEXTO, command=self.abrir_documento)
        self.btn_abrir_documento.grid(row=2, column=2, pady=6, padx=(10, 0), sticky="ew")  # de 3 a 2
        self.btn_abrir_documento.grid_remove()


        # Tabla
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        scroll = ttk.Scrollbar(tabla_frame)
        scroll.pack(side="right", fill="y")

        columnas = ("id", "fecha", "numero_factura", "pagada", "monto", "cliente", "abrir")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", yscrollcommand=scroll.set)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), anchor="w")
            self.tabla.column(col, width=120 if col != "abrir" else 80, anchor="w")

        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        self.tabla.bind("<Double-1>", self._click_en_abrir)


        # Total facturacion
        self.total_label = tk.Label(panel, text="Total Facturacion: ₡0.00", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        self.total_label.pack(pady=(5, 10), anchor="e", padx=20)

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

    def seleccionar_documento(self):
        ruta = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if ruta:
            with open(ruta, "rb") as f:
                self.documento_pdf = f.read()
            self.btn_documento.config(text=os.path.basename(ruta))

    def abrir_documento(self):
        if self.documento_pdf:
            self._abrir_documento_blob(self.documento_pdf)

    def _abrir_documento_blob(self, binario):
        try:
            ruta_temp = os.path.join(os.getcwd(), "temp_factura.pdf")
            with open(ruta_temp, "wb") as f:
                f.write(binario)
            os.startfile(ruta_temp)
        except Exception as e:
            mensajes.mensajes_Error(f"No se pudo abrir el documento: {e}")

    def cargar_facturas(self):
        self.tabla.delete(*self.tabla.get_children())
        self.documentos_en_memoria.clear()
        datos = self.model.mostrar_factura()
        if isinstance(datos, list):
            for fila in datos:
                # fila: (id, fecha, numero, pagada, monto, documento, cliente)
                self.documentos_en_memoria[fila[0]] = fila[5]
                self.tabla.insert("", "end", values=(
                    fila[0], fila[1], fila[2], "Sí" if fila[3] else "No", fila[4], fila[6], "Abrir"
                ))
        self.actualizar_total_factura()
        

    def aplicar_filtro(self):
        inicio = self.filtro_fecha_inicio.get()
        fin = self.filtro_fecha_fin.get()
        resultados = self.model.filtrar_factura_fecha(inicio, fin)
        self.tabla.delete(*self.tabla.get_children())
        self.documentos_en_memoria.clear()
        if isinstance(resultados, list):
            for fila in resultados:
                self.documentos_en_memoria[fila[0]] = fila[5]
                self.tabla.insert("", "end", values=(
                    fila[0], fila[1], fila[2], "Sí" if fila[3] else "No", fila[4], fila[6], "Abrir"
                ))

    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = valores[0]
            self.fecha.set_date(valores[1])
            self.entry_numero.delete(0, tk.END)
            self.entry_numero.insert(0, valores[2])
            self.entry_monto.delete(0, tk.END)
            self.entry_monto.insert(0, valores[4])
            self.combo_cliente.set(valores[5])
            self.documento_pdf = self.documentos_en_memoria.get(int(self.id_seleccionado))
            self.btn_abrir_documento.grid()

    def _click_en_abrir(self, event):
        region = self.tabla.identify("region", event.x, event.y)
        if region == "cell":
            fila = self.tabla.identify_row(event.y)
            columna = self.tabla.identify_column(event.x)
            if columna == "#7":
                item = self.tabla.item(fila)
                id_fila = item["values"][0]
                documento = self.documentos_en_memoria.get(int(id_fila))
                if documento:
                    self._abrir_documento_blob(documento)

    def guardar(self):
        self.model.guardar_factura(
            self.combo_cliente.get(),
            self.fecha.get(),
            self.entry_numero.get(),
            self.documento_pdf,
            self.entry_monto.get()
        )
        self.limpiar()

    def actualizar(self):
        self.model.actualizar_factura(
            self.id_seleccionado,
            self.combo_cliente.get(),
            self.fecha.get(),
            self.entry_numero.get(),
            self.documento_pdf,
            self.entry_monto.get()
        )
        self.limpiar()

    def eliminar(self):
        self.model.eliminar_factura(self.id_seleccionado)
        self.limpiar()

    def limpiar(self):
        self.id_seleccionado = None
        self.combo_cliente.set("")
        self.entry_numero.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)
        self.fecha.set_date(date.today())
        self.documento_pdf = None
        self.filtro_cliente.delete(0,tk.END)
        self.filtro_pagada.delete(0,tk.END)
        self.btn_documento.config(text="Seleccionar Documento")
        self.btn_abrir_documento.grid_remove()
        self.cargar_facturas()


    def aplicar_filtro_nombre_pagada(self):
        cliente = self.filtro_cliente.get()
        pagada = self.filtro_pagada.get()

        # Preparar valores
        cliente_valor = cliente if cliente else None
        if pagada == "Sí":
            pagada_valor = 1
        elif pagada == "No":
            pagada_valor = 0
        else:
            pagada_valor = None

        resultados = self.model.filtrar_factura_nombre_pagadas(cliente_valor, pagada_valor)

        self.tabla.delete(*self.tabla.get_children())
        self.documentos_en_memoria.clear()
        if isinstance(resultados, list):
            for fila in resultados:
                self.documentos_en_memoria[fila[0]] = fila[5]
                self.tabla.insert("", "end", values=(
                    fila[0], fila[1], fila[2], "Sí" if fila[3] else "No", fila[4], fila[6], "Abrir"
                ))

        self.actualizar_total_factura()


        
    def actualizar_total_factura(self):
        total = 0
        for child in self.tabla.get_children():
            monto_str = self.tabla.item(child)["values"][4]  # columna monto
            try:
                monto = float(monto_str)
                total += monto
            except (ValueError, TypeError):
                pass

        self.total_label.config(text=f"Total Facturas: ₡{total:,.2f}")
