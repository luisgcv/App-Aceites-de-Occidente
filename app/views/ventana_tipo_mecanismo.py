import tkinter as tk
from tkinter import ttk
from controllers import controlador_tipo_mecanismo as ctrl
from utils.mensajes import mensajes

# Colores y fuentes (los mismos)
COLOR_FONDO          = "#1B1F2A"
COLOR_PANEL          = "#252B3A"
COLOR_TEXTO          = "#FFFFFF"
COLOR_PRIMARIO       = "#2ECC71"
COLOR_PRIMARIO_OSCURO= "#27AE60"
COLOR_HOVER          = "#34D178"
COLOR_BORDE          = "#34495E"

FUENTE_TITULO  = ("Segoe UI", 18, "bold")
FUENTE_NORMAL  = ("Segoe UI", 11)
FUENTE_BOTON   = ("Segoe UI", 11, "bold")


class VentanaTipoMecanismoContacto(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)

        # Referencia al controlador
        self.tipo_model = ctrl
        self.id_seleccionado = None

        self._configurar_estilos()

        # ────────── Layout general ──────────
        container = tk.Frame(self, bg=COLOR_FONDO)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        panel_principal = tk.Frame(
            container, bg=COLOR_PANEL, bd=2, relief=tk.GROOVE,
            highlightbackground=COLOR_BORDE, highlightthickness=1
        )
        panel_principal.pack(fill="both", expand=True, padx=5, pady=5)

        # ────────── Título ──────────
        frame_titulo = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_titulo.pack(fill="x", pady=(10, 10), padx=20)

        tk.Label(
            frame_titulo, text="Gestión de Tipos de Mecanismo de Contacto",
            font=FUENTE_TITULO, bg=COLOR_PANEL, fg=COLOR_PRIMARIO
        ).pack(side="left")

        tk.Frame(frame_titulo, height=2, bg=COLOR_BORDE).pack(fill="x", pady=(5, 0))

        # ────────── Formulario ──────────
        frame_formulario = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_formulario.pack(fill="x", padx=20, pady=10)

        formulario = tk.Frame(frame_formulario, bg=COLOR_PANEL)
        formulario.pack(anchor="w", padx=10, pady=10)

        tk.Label(
            formulario, text="Descripción:", font=FUENTE_NORMAL,
            bg=COLOR_PANEL, fg=COLOR_TEXTO
        ).grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))

        self.entry_descripcion = tk.Entry(
            formulario, width=40, font=FUENTE_NORMAL,
            bg=COLOR_FONDO, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
            relief=tk.FLAT, highlightcolor=COLOR_PRIMARIO,
            highlightthickness=1, highlightbackground=COLOR_BORDE
        )
        self.entry_descripcion.grid(row=0, column=1, pady=8)

        # ────────── Tabla ──────────
        frame_tabla = tk.Frame(panel_principal, bg=COLOR_PANEL)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = ("id", "descripcion")
        self.tabla = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings",
            yscrollcommand=scrollbar.set
        )

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), anchor="w")
            self.tabla.column(col, width=150, anchor="w")

        self.tabla.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla.yview)

        self.cargar_tipos()

        # ────────── Botones ──────────
        boton_frame = tk.Frame(panel_principal, bg=COLOR_PANEL)
        boton_frame.pack(pady=(5, 15))

        self._crear_boton(boton_frame, "Guardar Tipo",    self.guardar_tipo)
        self._crear_boton(boton_frame, "Eliminar Tipo",   self.eliminar_tipo)
        self._crear_boton(boton_frame, "Actualizar Tipo", self.actualizar_tipo)
        self._crear_boton(boton_frame, "Limpiar",         self.limpiar)

        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

    # ──────────────────────────────────────────────────────────
    def _crear_boton(self, frame, texto, comando):
        b = tk.Button(
            frame, text=texto, bg=COLOR_PRIMARIO, fg=COLOR_TEXTO,
            font=FUENTE_BOTON, relief=tk.FLAT, command=comando,
            activebackground=COLOR_PRIMARIO_OSCURO, activeforeground=COLOR_TEXTO
        )
        b.pack(side="left", padx=10, ipadx=15, ipady=5)
        b.bind("<Enter>", lambda e: b.config(bg=COLOR_HOVER))
        b.bind("<Leave>", lambda e: b.config(bg=COLOR_PRIMARIO))

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure(
            "Treeview", background=COLOR_FONDO, foreground=COLOR_TEXTO,
            fieldbackground=COLOR_FONDO, borderwidth=0, font=FUENTE_NORMAL
        )
        estilo.configure(
            "Treeview.Heading", background=COLOR_BORDE,
            foreground=COLOR_TEXTO, font=FUENTE_BOTON, relief="flat"
        )
        estilo.map(
            "Treeview",
            background=[("selected", COLOR_PRIMARIO_OSCURO)],
            foreground=[("selected", COLOR_TEXTO)]
        )

    # ────────── Acciones CRUD ──────────
    def limpiar(self):
        self.cargar_tipos()
        self.id_seleccionado = None
        self.entry_descripcion.delete(0, tk.END)

    def cargar_tipos(self):
        self.tabla.delete(*self.tabla.get_children())
        datos = self.tipo_model.mostrar_tipos_mecanismo()
        if datos:
            if isinstance(datos, list):
                for fila in datos:
                    self.tabla.insert("", "end", values=fila)
            else:
                mensajes.mensajes_Error(f"No se pudieron cargar los tipos:\n{datos}")

    def guardar_tipo(self):
        self.tipo_model.guardar_tipo_mecanismo(self.entry_descripcion.get())
        self.limpiar()

    def eliminar_tipo(self):
        self.tipo_model.eliminar_tipo_mecanismo(self.id_seleccionado)
        self.limpiar()

    def actualizar_tipo(self):
        self.tipo_model.actualizar_tipo_mecanismo(
            self.id_seleccionado, self.entry_descripcion.get()
        )
        self.limpiar()

    # ────────── Seleccionar fila ──────────
    def _al_seleccionar(self, _event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.id_seleccionado = int(valores[0])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[1])
