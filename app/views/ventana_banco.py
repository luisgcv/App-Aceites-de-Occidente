import tkinter as tk
from tkinter import Canvas, ttk
from controllers import controlador_banco, controlador_party
from utils.mensajes import mensajes
from utils.pdf.pdf_exporter import exportar_pdf


# Colores y fuentes (igual que tu ventana Party y Mecanismo de Contacto)
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

class VentanaBanco(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.model = controlador_banco
        self.id_seleccionado = None

        self._configurar_estilos()
        self._construir_ui()
        self.cargar_bancos()


    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         fieldbackground=COLOR_FONDO, borderwidth=0, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", background=COLOR_BORDE, foreground=COLOR_TEXTO,
                         font=FUENTE_BOTON, relief="flat")
        estilo.map("Treeview", background=[("selected", COLOR_PRIMARIO_OSCURO)],
                   foreground=[("selected", COLOR_TEXTO)])
        estilo.configure("TSeparator", background=COLOR_BORDE)

        estilo.configure("TCombobox",
                         fieldbackground=COLOR_FONDO,
                         background=COLOR_FONDO,
                         foreground=COLOR_TEXTO,
                         selectbackground=COLOR_PRIMARIO_OSCURO,
                         selectforeground=COLOR_TEXTO)

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
            combo.set("Sin opciones")

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
        tk.Label(cabecera, text="Gestión de Bancos", font=FUENTE_TITULO,
                 bg=COLOR_PANEL, fg=COLOR_PRIMARIO).pack(side="left")
        tk.Frame(cabecera, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(5, 0))

        form_wrapper = tk.Frame(panel, bg=COLOR_PANEL)
        form_wrapper.pack(fill="x", padx=20, pady=10)
        form = tk.Frame(form_wrapper, bg=COLOR_PANEL)
        form.pack(anchor="w", padx=10, pady=10)

        # Lista manual con nombres de bancos
        nombres_banco = [
            "Banco Nacional de Costa Rica (BN)",
            "Banco de Costa Rica (BCR)",
            "Banco Popular y de Desarrollo Comunal (BP)",
            "Banco Lafise Bancentro",
            "Scotiabank Costa Rica",
            "Davivienda Costa Rica",
            "BAC Credomatic",
            "Banco General (Costa Rica)",
            "Citibank Costa Rica",
            "Banco Promerica",
        ]


        tk.Label(form, text="Nombre Banco:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))

        self.combo_nombre_banco = self._crear_combo(form, nombres_banco)
        self.combo_nombre_banco.grid(row=0, column=1, pady=6)


        # Cuenta IBAN
        tk.Label(form, text="Cuenta IBAN:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_cuenta_iban = tk.Entry(form, width=40, font=FUENTE_NORMAL, bg=COLOR_FONDO,
                                   fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                   relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                   highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_cuenta_iban.grid(row=1, column=1, pady=6)

        # Cuenta Cliente
        tk.Label(form, text="Cuenta Cliente(opcional):", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_cuenta_cliente = tk.Entry(form, width=40, font=FUENTE_NORMAL, bg=COLOR_FONDO,
                                   fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                   relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
                                   highlightthickness=1, highlightbackground=COLOR_BORDE)
        self.entry_cuenta_cliente.grid(row=2, column=1, pady=6)

        # Persona / Party
        tk.Label(form, text="Persona:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO)\
            .grid(row=3, column=0, sticky="w", pady=6, padx=(0, 10))
        parties = controlador_party.mostrar_personas()
        self.combo_party = self._crear_combo(form, parties)
        self.combo_party.grid(row=3, column=1, pady=6)

        # Frame filtros (parte derecha)
        filtro_frame = tk.Frame(cabecera, bg=COLOR_PANEL)
        filtro_frame.pack(side="right")

        # Filtro por Nombre Banco (Entry para texto libre)
        tk.Label(filtro_frame, text="Nombre Banco:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))

        self.combo_nombre_banco_filtro = ttk.Combobox(filtro_frame, values=nombres_banco, state="readonly",
                                                    width=40, font=FUENTE_NORMAL)
        self.combo_nombre_banco_filtro.pack(side="left", padx=(0, 15), ipady=2)

        # Opcionalmente poner un valor por defecto o texto:
        if nombres_banco:
            self.combo_nombre_banco_filtro.current(0)
        else:
            self.combo_nombre_banco_filtro.set("Sin opciones")

        # Filtro por Persona / Party (Combobox)
        tk.Label(filtro_frame, text="Persona:", font=FUENTE_NORMAL, bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=(0, 5))
        parties_filtro = controlador_party.mostrar_personas()
        self.combo_filtro_party = self._crear_combo(filtro_frame, parties_filtro)
        self.combo_filtro_party.config(width=30)
        self.combo_filtro_party.pack(side="left", padx=(0, 15), ipady=2)

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
        columnas = ("banco_id", "nombre_banco", "cuenta_iban", "cuenta_cliente", "nombre_party")
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
        self._crear_boton(btn_frame, "Guardar", self.guardar_banco).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Actualizar", self.actualizar_banco).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Eliminar", self.eliminar_banco).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Limpiar", self.limpiar).pack(side="left", padx=10)
        self._crear_boton(btn_frame, "Exportar", self.exportar_banco_pdf).pack(side="left", padx=10)


    def _crear_boton(self, master, texto, comando):
        btn = tk.Button(master, text=f"{texto} Banco", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
                        font=FUENTE_BOTON, relief=tk.FLAT, activebackground=COLOR_PRIMARIO_OSCURO,
                        activeforeground=COLOR_TEXTO, command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARIO))
        return btn

    def limpiar(self):
        self.id_seleccionado = None

        # Para combo_nombre_banco (ComboBox)
        if self.combo_nombre_banco["state"] == "readonly" and self.combo_nombre_banco['values']:
            self.combo_nombre_banco.current(0)
        else:
            self.combo_nombre_banco.set("")

        # Para entries de cuenta iban y cuenta cliente
        self.entry_cuenta_iban.delete(0, tk.END)
        self.entry_cuenta_cliente.delete(0, tk.END)

        # Combo party
        if self.combo_party["state"] == "readonly" and self.combo_party['values']:
            self.combo_party.current(0)
        else:
            self.combo_party.set("")

        # Filtros

        # Cambiado: combo_nombre_banco_filtro es Combobox, no Entry
        if self.combo_nombre_banco_filtro["state"] == "readonly" and self.combo_nombre_banco_filtro['values']:
            self.combo_nombre_banco_filtro.current(0)
        else:
            self.combo_nombre_banco_filtro.set("")

        if self.combo_filtro_party["state"] == "readonly" and self.combo_filtro_party['values']:
            self.combo_filtro_party.current(0)
        else:
            self.combo_filtro_party.set("")


        self.cargar_bancos()

    def cargar_bancos(self):
        self.tabla.delete(*self.tabla.get_children())
        datos = self.model.mostrar_banco()
        if isinstance(datos, list):
            for fila in datos:
                self.tabla.insert(
                    "", "end",
                    values=(fila[0], fila[1], fila[2], fila[3], fila[5])
                )
        elif datos is not None:
            mensajes.mensajes_Error
            
    def _al_seleccionar(self, _event):
        item = self.tabla.focus()
        if item:
            val = self.tabla.item(item, "values")

            # 0) ID seleccionado
            self.id_seleccionado = int(val[0])

            # 1) Nombre Banco (ComboBox)
            self.combo_nombre_banco.set(val[1])

            # 2) Cuenta IBAN (Entry)
            self.entry_cuenta_iban.delete(0, tk.END)
            self.entry_cuenta_iban.insert(0, val[2])

            # 3) Cuenta Cliente (Entry)
            self.entry_cuenta_cliente.delete(0, tk.END)
            self.entry_cuenta_cliente.insert(0, val[3])

            # 4) Persona / Party (ComboBox)
            self.combo_party.set(val[4])



    def guardar_banco(self):
        self.model.guardar_banco(
            self.combo_nombre_banco.get(),
            self.entry_cuenta_iban.get(),
            self.entry_cuenta_cliente.get(),
            self.combo_party.get()
        )
        self.limpiar()


    def actualizar_banco(self):
        self.model.actualizar_banco(
            self.id_seleccionado,
            self.combo_nombre_banco.get(),
            self.entry_cuenta_iban.get(),
            self.entry_cuenta_cliente.get(),
            self.combo_party.get()
        )
        self.limpiar()


    def eliminar_banco(self):
        self.model.eliminar_banco(self.id_seleccionado)
        self.limpiar()





    def aplicar_filtro(self):
        nombre_banco = self.combo_nombre_banco_filtro.get()
        nombre_party = self.combo_filtro_party.get()

        resultados = self.model.filtrar_banco(nombre_banco, nombre_party)

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        if isinstance(resultados, list):
            for item in resultados:
                self.tabla.insert("", "end", values=item)
        elif resultados is not None:
            mensajes.mensajes_Error(f"Error al filtrar:\n{resultados}")

    def exportar_banco_pdf(self):
        filas = self.tabla.get_children()

        # Obtiene solo las columnas que deseas: desde la segunda posición (índice 1)
        datos = [self.tabla.item(fila)["values"][1:] for fila in filas]

        # Encabezados correspondientes a las columnas que sí deseas mostrar
        columnas = ["Nombre Banco", "Cuenta IBAN", "Cuenta Cliente", "Persona"]

        exportar_pdf(datos, columnas, titulo="Listado de Bancos por Persona")
