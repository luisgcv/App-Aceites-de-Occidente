import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from .ventana_banco import VentanaBanco
from .ventana_party import VentanaParty
from .ventana_naturaleza_persona import VentanaNaturalezaPersona
from .ventana_nacionalidad import VentanaNacionalidad
from .ventana_puesto import VentanaPuestoTrabajo
from .ventana_tipo_identificacion import VentanaTipoIdentificacion
from .ventana_tipo_mecanismo import VentanaTipoMecanismoContacto
from .ventana_metodo_pago import VentanaMetodoPago
from .ventana_identificaciones import VentanaIdentificacion
from .ventana_mecanismo_contacto import VentanaMecanismoContacto
from .ventana_relacion_puesto import VentanaRelacionPuesto
from .ventana_empleado import VentanaEmpleado
from .ventana_planilla import VentanaPlanilla
from .ventana_estado_cuenta import VentanaEstadoCuenta
from .ventana_retiro import VentanaRetiro
from .ventana_ingreso import VentanaIngresos
from .ventana_factura import VentanaFactura
from .ventana_gasto import VentanaGasto
from .ventana_transaccion import VentanaTransaccion
from .ventana_inicio import VentanaInicio
from .ventana_reporte import VentanaReportes

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

# Fuentes actualizadas
FUENTE_TITULO = ("Segoe UI", 18, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 14)
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")
FUENTE_MENU = ("Segoe UI", 11)


class AppBase(tk.Tk):
    def __init__(self, rol, logo_path=None):
        super().__init__()

        # Maximizar ventana al iniciar
        self.state("zoomed")  # En Windows
        # Para Linux/Mac a veces funciona mejor:
        # self.attributes('-zoomed', True)

        # Título y fondo
        self.title("Sistema de Gestión - Aceites De Occidente y La Bajura")
        self.configure(bg=COLOR_FONDO)

        # Tamaño mínimo para evitar que se haga demasiado pequeña
        self.minsize(600, 400)
        self.title("Sistema de Gestión - Aceites De Occidente y La Bajura")
        self.configure(bg=COLOR_FONDO)

        # Estilo mejorado
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self.configurar_estilos()

        # Frame principal con grid mejorado
        self.main_frame = tk.Frame(self, bg=COLOR_FONDO)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.main_frame.columnconfigure(0, weight=0, minsize=240)  # Menú más ancho
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Menú principal con estilos consistentes
        barra_menu = tk.Menu(
            self,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            activebackground=COLOR_PRIMARIO_OSCURO,
            activeforeground=COLOR_TEXTO,
            tearoff=0,
            font=FUENTE_NORMAL
        )

            # Menú Catálogos
        menu_catalogos = tk.Menu(barra_menu, tearoff=0, bg=COLOR_PANEL, fg=COLOR_TEXTO, activebackground=COLOR_PRIMARIO, activeforeground=COLOR_TEXTO, font=FUENTE_NORMAL)
        menu_catalogos.add_command(label="Naturaleza de Persona", command=self.mostrar_naturaleza_party)
        menu_catalogos.add_command(label="Nacionalidades", command=self.mostrar_nacionalidades)
        menu_catalogos.add_command(label="Puestos de Trabajo", command=self.mostrar_puestos)
        menu_catalogos.add_command(label="Tipos de Identificación", command=self.mostrar_tipo_identificacion)
        menu_catalogos.add_command(label="Tipos de Contacto", command=self.mostrar_tipo_medio_contacto)
        menu_catalogos.add_command(label="Métodos de Pago", command=self.mostrar_metodos_pago)

        # Menú Gestión de Personas
        menu_personas = tk.Menu(barra_menu, tearoff=0, bg=COLOR_PANEL, fg=COLOR_TEXTO, activebackground=COLOR_PRIMARIO, activeforeground=COLOR_TEXTO, font=FUENTE_NORMAL)
        menu_personas.add_command(label="Personas / Entidades", command=self.mostrar_party)
        menu_personas.add_command(label="Identificaciones", command=self.mostrar_identificaciones)
        menu_personas.add_command(label="Medios de Contacto", command=self.mostrar_medios_contacto)
        menu_personas.add_command(label="Asignación de Puestos", command=self.mostrar_relacion_puesto_trabajo)

        #Menu Empleados
        menu_empleados = tk.Menu(barra_menu, tearoff=0, bg=COLOR_PANEL, fg=COLOR_TEXTO, activebackground=COLOR_PRIMARIO, activeforeground=COLOR_TEXTO, font=FUENTE_NORMAL)
        menu_empleados.add_command(label="Empleados", command=self.mostrar_gestion_empleados)
        menu_empleados.add_command(label="Planilla", command=self.mostrar_planilla)



        # Menú Gestión Financiera
        menu_finanzas = tk.Menu(barra_menu, tearoff=0, bg=COLOR_PANEL, fg=COLOR_TEXTO, activebackground=COLOR_PRIMARIO, activeforeground=COLOR_TEXTO, font=FUENTE_NORMAL)
        menu_finanzas.add_command(label="Bancos", command=self.mostrar_gestion_bancos)
        menu_finanzas.add_command(label="Retiros", command=self.mostrar_retiros)
        menu_finanzas.add_command(label="Ingresos", command=self.mostrar_ingresos)
        menu_finanzas.add_command(label="Estados de Cuenta", command=self.mostrar_estado_cuenta)


        # Menú Sistema
        menu_sistema = tk.Menu(barra_menu, tearoff=0, bg=COLOR_PANEL, fg=COLOR_TEXTO, activebackground=COLOR_PRIMARIO, activeforeground=COLOR_TEXTO, font=FUENTE_NORMAL)
        menu_sistema.add_command(label="Salir", command=self.salir)

        # Agregar a la barra principal
        barra_menu.add_cascade(label="Catálogos", menu=menu_catalogos)
        barra_menu.add_cascade(label="Gestión de Personas", menu=menu_personas)
        barra_menu.add_cascade(label="Gestión Financiera", menu=menu_finanzas)
        barra_menu.add_cascade(label="Gestión Empleados", menu=menu_empleados)
        barra_menu.add_cascade(label="Sistema", menu=menu_sistema)


        # Configurar la barra de menú en la ventana
        self.config(menu=barra_menu)

        # Menú lateral 
        self.menu_frame = tk.Frame(
            self.main_frame, 
            bg=COLOR_PANEL, 
            width=240,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        self.menu_frame.grid(row=0, column=0, sticky="nswe", padx=(0, 5))
        self.menu_frame.grid_propagate(False)
        self.crear_menu_lateral_en(self.menu_frame, logo_path)

        # Contenido con borde sutil
        self.contenido_frame = tk.Frame(
            self.main_frame, 
            bg=COLOR_PANEL,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        self.contenido_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Barra de estado mejorada
        self.barra_estado = tk.Label(
            self,
            text=f"Usuario: {rol} | Sistema de Gestión Aceites de Occidente y la Bajura",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SEC,
            font=FUENTE_NORMAL,
            padx=10
        )
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

        # Vista inicial
        self.mostrar_inicio()

    def configurar_estilos(self):
        # Configuración de estilos mejorada
        self.estilo.configure('TButton',
            font=FUENTE_BOTON,
            background=COLOR_PRIMARIO,
            foreground=COLOR_TEXTO,
            borderwidth=0,
            padding=8,
            relief="flat",
            focusthickness=0,
            focuscolor='none',
            bordercolor=COLOR_PRIMARIO,
            lightcolor=COLOR_PRIMARIO,
            darkcolor=COLOR_PRIMARIO_OSCURO
        )
        self.estilo.map('TButton',
            background=[
                ('active', COLOR_HOVER), 
                ('pressed', COLOR_PRIMARIO_OSCURO)
            ],
            foreground=[
                ('active', COLOR_TEXTO), 
                ('pressed', COLOR_TEXTO)
            ]
        )
        
        # Estilo para frames
        self.estilo.configure('TFrame', 
            background=COLOR_PANEL,
            relief="flat"
        )
        
        # Estilo para labels
        self.estilo.configure('TLabel', 
            background=COLOR_PANEL, 
            foreground=COLOR_TEXTO,
            font=FUENTE_NORMAL
        )
        
        # Estilo para el menú
        self.estilo.configure('Menu.TButton',
            font=FUENTE_MENU,
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO,
            padding=10,
            relief="flat"
        )
        self.estilo.map('Menu.TButton',
            background=[
                ('active', COLOR_PRIMARIO), 
                ('pressed', COLOR_PRIMARIO_OSCURO)
            ],
            foreground=[
                ('active', COLOR_TEXTO), 
                ('pressed', COLOR_TEXTO)
            ]
        )

        self.protocol("WM_DELETE_WINDOW", self.salir)


    def crear_menu_lateral_en(self, frame, logo_path):

        # Contenedor del logo 
        logo_container = tk.Frame(
            frame, 
            bg=COLOR_PANEL,
            padx=10,
            pady=20
        )
        logo_container.pack(fill="x")

        if logo_path:
            try:
                img = Image.open(logo_path)
                img = img.resize((100, 100), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                logo_label = tk.Label(
                    logo_container, 
                    image=self.logo_img, 
                    bg=COLOR_PANEL
                )
                logo_label.pack()
            except:
                logo_label = tk.Label(
                    logo_container, 
                    text="LOGO", 
                    bg=COLOR_PANEL, 
                    fg=COLOR_PRIMARIO, 
                    font=FUENTE_TITULO
                )
                logo_label.pack()
        else:
            logo_label = tk.Label(
                logo_container, 
                text="LOGO", 
                bg=COLOR_PANEL, 
                fg=COLOR_PRIMARIO, 
                font=FUENTE_TITULO
            )
            logo_label.pack()

        # Separador
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

        opciones_menu = [
            ("Inicio", "home", self.mostrar_inicio),

            # Gestión operativa
            ("Empleados", "id-card", self.mostrar_gestion_empleados),
            ("Facturación", "file-text", self.mostrar_facturacion),
            ("Gastos", "wallet", self.mostrar_gasto),
            ("Transacciones", "exchange-alt", self.mostrar_transacciones),

            # Bancos y estado de cuenta
            ("Gestión Bancos", "university", self.mostrar_gestion_bancos),

            # Reportes y salida
            ("Reportes", "bar-chart", self.mostrar_reportes),
            ("Salir", "power-off", self.salir)
        ]


        for texto, icono, comando in opciones_menu:
            btn = ttk.Button(
                frame,
                text=f"  {texto}",
                style='Menu.TButton',
                command=comando
            )
            btn.pack(fill="x", pady=2, padx=10, ipady=8)

    def mostrar_inicio(self):
        self.limpiar_contenido()
        vista = VentanaInicio(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)



    def mostrar_transacciones(self):
        self.limpiar_contenido()
        vista = VentanaTransaccion(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)


    def mostrar_gestion_bancos(self):
        self.limpiar_contenido()
        vista = VentanaBanco(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)


    def mostrar_retiros(self):
        self.limpiar_contenido()
        vista = VentanaRetiro(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

    def mostrar_gestion_empleados(self):
        self.limpiar_contenido()
        vista = VentanaEmpleado(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

 

    def mostrar_facturacion(self):
        self.limpiar_contenido()
        vista = VentanaFactura(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)    

    def mostrar_reportes(self):
        self.limpiar_contenido()
        vista = VentanaReportes(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)    



    def mostrar_planilla(self): 
        self.limpiar_contenido()
        vista = VentanaPlanilla(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)
    

    def mostrar_ingresos(self): 
        self.limpiar_contenido()
        vista = VentanaIngresos(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)


    def mostrar_party(self): 
        self.limpiar_contenido()
        vista = VentanaParty(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)
    
    def mostrar_identificaciones(self): 
        self.limpiar_contenido()
        vista = VentanaIdentificacion(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

    
    def mostrar_medios_contacto(self): 
        self.limpiar_contenido()
        vista = VentanaMecanismoContacto(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

 

    def mostrar_relacion_puesto_trabajo(self): 
        self.limpiar_contenido()
        vista = VentanaRelacionPuesto(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)


    def mostrar_puestos(self): 
        self.limpiar_contenido()
        vista = VentanaPuestoTrabajo(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)


    def mostrar_naturaleza_party(self): 
        self.limpiar_contenido()
        vista = VentanaNaturalezaPersona(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

    

    def mostrar_nacionalidades(self): 
        self.limpiar_contenido()
        vista = VentanaNacionalidad(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

    

    def mostrar_metodos_pago(self): 
        self.limpiar_contenido()
        vista = VentanaMetodoPago(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)
  

    def mostrar_tipo_identificacion(self): 
        self.limpiar_contenido()
        vista = VentanaTipoIdentificacion(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

    def mostrar_gasto(self): 
        self.limpiar_contenido()
        vista = VentanaGasto(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

        
        
    def mostrar_tipo_medio_contacto(self): 
        self.limpiar_contenido()
        vista = VentanaTipoMecanismoContacto(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)

    
    def mostrar_estado_cuenta(self): 
        self.limpiar_contenido()
        vista = VentanaEstadoCuenta(self.contenido_frame)
        vista.pack(fill="both", expand=True, padx=20, pady=20)
      

    def limpiar_contenido(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()

    def salir(self):
        if messagebox.askyesno(
            "Confirmar salida",
            "¿Está seguro que desea salir de la aplicación?",
            icon='question'
        ):
            self.quit()       # Termina el mainloop
            self.destroy()    # Destruye la ventana principal