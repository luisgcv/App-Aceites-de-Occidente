import tkinter as tk
from tkinter import Canvas, ttk
from controllers import controlador_dashboard
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# Paleta de colores
COLOR_FONDO = "#1B1F2A"
COLOR_PANEL = "#252B3A"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_SEC = "#B0B4C8"
COLOR_PRIMARIO = "#2ECC71"
COLOR_PRIMARIO_OSCURO = "#27AE60"
COLOR_HOVER = "#34D178"
COLOR_BOTON = COLOR_PRIMARIO
COLOR_BOTON_SEC = "#3498db"
COLOR_BORDE = "#3D4354"

# Fuentes
FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")


class VentanaInicio(tk.Frame):
    def __init__(self, master=None):
            super().__init__(master, bg=COLOR_FONDO)
            self.pack(fill="both", expand=True)
            self.config(padx=20, pady=20)

            # Canvas + Scrollbar
            self.canvas = tk.Canvas(self, bg=COLOR_FONDO, highlightthickness=0)
            self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)

            # Frame dentro del canvas donde irá todo el contenido
            self.main_container = tk.Frame(self.canvas, bg=COLOR_FONDO)
            
            # Crear ventana interior en canvas
            self.canvas_frame = self.canvas.create_window((0,0), window=self.main_container, anchor="nw")

            # Ajustar el scroll del canvas cuando cambia tamaño el contenido
            self.main_container.bind("<Configure>", self._on_frame_configure)
            self.canvas.bind("<Configure>", self._on_canvas_configure)

            self.crear_tarjetas_resumen()
            self.crear_grafico_ingresos_gastos()
            self.crear_facturas_pendientes()



    def _on_frame_configure(self, event):
        # Ajusta el scrollregion del canvas a todo el tamaño del frame interno
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Mantiene el ancho del frame interno igual al ancho visible del canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def crear_tarjetas_resumen(self):
        frame_tarjetas = tk.Frame(self.main_container, bg=COLOR_FONDO)
        frame_tarjetas.pack(fill="x", pady=(0, 20))
        
        datos = {
            "Total Gastos (Mes)": controlador_dashboard.mostrar_total_gastos_mes(),
            "Total Ingresos (Mes)": controlador_dashboard.mostrar_ingresos_mensuales(),
            "Facturas Pendientes": controlador_dashboard.mostrar_factura_pendiente(),
            "Transacciones Recientes": controlador_dashboard.mostrar_transacciones_recientes(),
        }

        for idx, (titulo, valor) in enumerate(datos.items()):
            # Frame de la tarjeta
            tarjeta = tk.Frame(
                frame_tarjetas, 
                bg=COLOR_PANEL, 
                bd=0, 
                relief="flat",
                highlightbackground=COLOR_BORDE,
                highlightthickness=1,
                padx=15,
                pady=10
            )
            tarjeta.grid(row=0, column=idx, padx=10, sticky="nsew")
            frame_tarjetas.columnconfigure(idx, weight=1)
            
            # Icono (simulado con texto)
            icono = tk.Label(
                tarjeta, 
                text="•", 
                font=("Segoe UI", 24), 
                fg=COLOR_PRIMARIO, 
                bg=COLOR_PANEL
            )
            icono.pack(anchor="w")
            
            # Título
            label_titulo = tk.Label(
                tarjeta, 
                text=titulo, 
                font=("Segoe UI", 10), 
                fg=COLOR_TEXTO_SEC, 
                bg=COLOR_PANEL,
                anchor="w"
            )
            label_titulo.pack(fill="x")
            
            # Valor
            if isinstance(valor, list):
                cantidad = len(valor)
            elif isinstance(valor, str):
                cantidad = valor
            elif valor:
                cantidad = valor[-1]["total_ingresos"] if "ingresos" in titulo.lower() else valor[-1]["total_gastos"]
            else:
                cantidad = "0"
                
            label_valor = tk.Label(
                tarjeta, 
                text=cantidad, 
                font=("Segoe UI", 18, "bold"), 
                fg=COLOR_TEXTO, 
                bg=COLOR_PANEL,
                anchor="w"
            )
            label_valor.pack(fill="x")

    def crear_grafico_ingresos_gastos(self):
        frame_grafico = tk.Frame(self.main_container, bg=COLOR_FONDO)
        frame_grafico.pack(fill="x", pady=(0, 20))
        
        # Título del gráfico
        titulo_grafico = tk.Label(
            frame_grafico,
            text="Historial de Ingresos vs Gastos",
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            anchor="w"
        )
        titulo_grafico.pack(fill="x", pady=(0, 10))
        
        # Contenedor del gráfico
        contenedor_grafico = tk.Frame(
            frame_grafico, 
            bg=COLOR_PANEL,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1,
            padx=5,
            pady=5
        )
        contenedor_grafico.pack(fill="both", expand=True)
        
        data_ingresos = controlador_dashboard.mostrar_ingresos_mensuales() or []
        data_gastos = controlador_dashboard.mostrar_total_gastos_mes() or []

        ingresos_dict = {mes: monto for mes, monto in data_ingresos}
        gastos_dict = {mes: monto for mes, monto in data_gastos}
        meses = sorted(set(ingresos_dict.keys()) | set(gastos_dict.keys()))
        
        # Estilo del gráfico
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100, facecolor=COLOR_PANEL)
        ax.set_facecolor(COLOR_PANEL)
        
        x = range(len(meses))
        ax.bar(
            [i - 0.2 for i in x], 
            [ingresos_dict.get(m, 0) for m in meses], 
            width=0.4, 
            label='Ingresos', 
            color=COLOR_PRIMARIO
        )
        ax.bar(
            [i + 0.2 for i in x], 
            [gastos_dict.get(m, 0) for m in meses], 
            width=0.4, 
            label='Gastos', 
            color="#E74C3C"  # Rojo para gastos
        )
        
        # Configuración de ejes
        ax.set_xticks(x)
        ax.set_xticklabels(meses, rotation=45, color=COLOR_TEXTO)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ax.get_yticks(), color=COLOR_TEXTO)
        
        # Títulos y leyenda
        ax.set_title('', color=COLOR_TEXTO, pad=20)
        ax.legend(facecolor=COLOR_PANEL, edgecolor=COLOR_BORDE, labelcolor=COLOR_TEXTO)
        
        # Grid y bordes
        ax.grid(True, linestyle='--', alpha=0.3, color=COLOR_BORDE)
        for spine in ax.spines.values():
            spine.set_color(COLOR_BORDE)
        
        # Integración con Tkinter
        canvas = FigureCanvasTkAgg(fig, master=contenedor_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def crear_facturas_pendientes(self):
        frame_facturas = tk.Frame(self.main_container, bg=COLOR_FONDO)
        frame_facturas.pack(fill="both", expand=True)
        
        # Título de la sección
        titulo_facturas = tk.Label(
            frame_facturas,
            text="Facturas Pendientes",
            font=FUENTE_TITULO,
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            anchor="w"
        )
        titulo_facturas.pack(fill="x", pady=(0, 10))
        
        # Contenedor del Treeview
        contenedor_tabla = tk.Frame(
            frame_facturas, 
            bg=COLOR_PANEL,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1,
            padx=5,
            pady=5
        )
        contenedor_tabla.pack(fill="both", expand=True)
        
        # Configuración del Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Treeview",
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO,
            fieldbackground=COLOR_PANEL,
            borderwidth=0,
            font=FUENTE_NORMAL
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_PRIMARIO_OSCURO,
            foreground=COLOR_TEXTO,
            font=FUENTE_BOTON,
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[('selected', COLOR_PRIMARIO)]
        )
        
        columns = ("Factura", "Cliente", "Fecha", "Monto")
        tree = ttk.Treeview(
            contenedor_tabla, 
            columns=columns, 
            show="headings",
            selectmode="extended",
            style="Treeview"
        )
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Insertar datos
        data = controlador_dashboard.mostrar_factura_pendiente() or []
        for f in data:
            tree.insert("", "end", values=(f[1], f[4], f[2], f[3]))
