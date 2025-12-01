import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
import os
from datetime import date

from controllers import controlador_estado_cuenta, controlador_banco
from utils.mensajes import mensajes

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

class VentanaEstadoCuenta(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_estado_cuenta
        self.id_seleccionado = None
        self.ruta_documento = None
        self.documentos_en_memoria = {}

        self._configurar_estilos()
        self._construir_ui()
        self.cargar_estado_cuenta()

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

        cabecera = tk.Frame(panel, bg=COLOR_PANEL)
        cabecera.pack(fill="x", pady=10, padx=20)
        tk.Label(cabecera, text="Estado de Cuenta", font=FUENTE_TITULO,
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

        form = tk.Frame(panel, bg=COLOR_PANEL)
        form.pack(fill="x", padx=20, pady=10)
        # Fila 0: Banco y Documento
        tk.Label(form, text="Banco:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        bancos = [b[2] for b in controlador_banco.mostrar_banco()]
        self.combo_banco = self._crear_combo(form, bancos)
        self.combo_banco.grid(row=0, column=1, pady=6, sticky="ew")

        tk.Label(form, text="Documento:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=2, sticky="w", pady=6, padx=(10, 10))
        self.btn_documento = tk.Button(form, text="Seleccionar Documento", font=FUENTE_NORMAL,
                                    bg=COLOR_ACCION, fg=COLOR_TEXTO, command=self.seleccionar_documento)
        self.btn_documento.grid(row=0, column=3, pady=6, sticky="ew")

        self.btn_abrir_documento = tk.Button(form, text="Abrir Documento", font=FUENTE_NORMAL,
                                     bg=COLOR_ACCION, fg=COLOR_TEXTO, command=self.abrir_documento)
        self.btn_abrir_documento.grid(row=0, column=4, pady=6, padx=(10, 0), sticky="ew")
        self.btn_abrir_documento.grid_remove()  # Ocultar al inicio

        # Fila 1: Fecha Inicio y Fecha Fin
        tk.Label(form, text="Fecha Inicio:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        self.fecha_inicio = DateEntry(form, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.fecha_inicio.grid(row=1, column=1, pady=6, sticky="ew")

        tk.Label(form, text="Fecha Fin:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=2, sticky="w", pady=6, padx=(10, 10))
        self.fecha_fin = DateEntry(form, font=FUENTE_NORMAL, date_pattern='yyyy-mm-dd')
        self.fecha_fin.grid(row=1, column=3, pady=6, sticky="ew")

        # Tabla
        tabla_frame = tk.Frame(panel, bg=COLOR_PANEL)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        scroll = ttk.Scrollbar(tabla_frame)
        scroll.pack(side="right", fill="y")

        columnas = ("id", "fecha_inicio", "fecha_fin", "banco", "cuenta_iban", "abrir")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", yscrollcommand=scroll.set)

        for col in columnas:
            self.tabla.heading(col, text=col.replace("_", " ").capitalize(), anchor="w")
            self.tabla.column(col, width=120 if col != "abrir" else 80, anchor="w")

        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        self.tabla.bind("<Double-1>", self._click_en_abrir)

        # Botones
        btn_frame = tk.Frame(panel, bg=COLOR_PANEL)
        btn_frame.pack(pady=10)
        self._crear_boton(btn_frame, "Guardar", self.guardar_estado_cuenta).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Actualizar", self.actualizar_estado_cuenta).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Eliminar", self.eliminar_estado_cuenta).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Limpiar", self.limpiar).pack(side="left", padx=10)

    def _crear_boton(self, master, texto, comando):
        btn = tk.Button(master, text=texto, bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                        font=FUENTE_BOTON, relief=tk.FLAT, activebackground=COLOR_PRIMARIO_OSCURO,
                        activeforeground=COLOR_TEXTO, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARIO))
        return btn

    def seleccionar_documento(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            with open(ruta, "rb") as f:
                self.ruta_documento = f.read()
            self.btn_documento.config(text=ruta.split("/")[-1])
            

    def cargar_estado_cuenta(self):
        self.tabla.delete(*self.tabla.get_children())
        self.documentos_en_memoria.clear()
        datos = self.model.mostrar_estado_cuenta()
        if isinstance(datos, list):
            for fila in datos:
                # fila: (id, fecha_inicio, fecha_fin, banco, cuenta_iban, documento_blob)
                self.documentos_en_memoria[fila[0]] = fila[5]
                self.tabla.insert("", "end", values=(fila[0], fila[1], fila[2], fila[3], fila[4], "Abrir"))

    def aplicar_filtro(self):
        inicio = self.filtro_fecha_inicio.get()
        fin = self.filtro_fecha_fin.get()
        resultados = self.model.filtrar_estado_cuenta(inicio, fin)
        self.tabla.delete(*self.tabla.get_children())
        self.documentos_en_memoria.clear()
        if isinstance(resultados, list):
            for fila in resultados:
                self.documentos_en_memoria[fila[0]] = fila[5]
                self.tabla.insert("", "end", values=(fila[0], fila[1], fila[2], fila[3], fila[4], "Abrir"))

    def _al_seleccionar(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = valores[0]
            self.fecha_inicio.set_date(valores[1])
            self.fecha_fin.set_date(valores[2])
            self.combo_banco.set(valores[4])
            self.ruta_documento = self.documentos_en_memoria.get(int(self.id_seleccionado))
            self.btn_abrir_documento.grid()  # Mostrar el botón "Abrir Documento"
                        

    def _click_en_abrir(self, event):
        region = self.tabla.identify("region", event.x, event.y)
        if region == "cell":
            fila = self.tabla.identify_row(event.y)
            columna = self.tabla.identify_column(event.x)
            if columna == "#6":  # columna "abrir"
                item = self.tabla.item(fila)
                id_fila = item["values"][0]
                documento = self.documentos_en_memoria.get(int(id_fila))
                if documento:
                    self._abrir_documento_blob(documento)

    def _abrir_documento_blob(self, binario):
        try:
            ruta_temp = os.path.join(os.getcwd(), "documento_temp.pdf")
            with open(ruta_temp, "wb") as f:
                f.write(binario)
            os.startfile(ruta_temp)
        except Exception as e:
            mensajes.mensajes_Error(f"No se pudo abrir el documento: {e}")

    def abrir_documento(self):
        if self.ruta_documento:
            self._abrir_documento_blob(self.ruta_documento)
        else:
            mensajes.mensajes_Error("No se ha cargado un documento.")

    def guardar_estado_cuenta(self):
        self.model.guardar_estado_cuenta(
            self.combo_banco.get(), self.fecha_inicio.get(), self.fecha_fin.get(), self.ruta_documento
        )
        self.limpiar()

    def actualizar_estado_cuenta(self):
        self.model.actualizar_estado_cuenta(
            self.id_seleccionado, self.combo_banco.get(), self.fecha_inicio.get(),
            self.fecha_fin.get(), self.ruta_documento
        )
        self.limpiar()

    def eliminar_estado_cuenta(self):
        self.model.eliminar_estado_cuenta(self.id_seleccionado)
        self.limpiar()

    def limpiar(self):
        self.id_seleccionado = None
        self.ruta_documento = None
        self.combo_banco.set("")
        self.fecha_inicio.set_date(date.today())
        self.fecha_fin.set_date(date.today())
        self.btn_documento.config(text="Seleccionar Documento", command=self.seleccionar_documento)
        self.cargar_estado_cuenta()
        self.btn_abrir_documento.grid_remove()  # Ocultar el botón al limpiar

