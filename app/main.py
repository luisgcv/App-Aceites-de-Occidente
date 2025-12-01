from views.ventana_base import AppBase
import tkinter as tk
from tkinter import messagebox
import traceback
from config.settings import obtener_conexion
import time
import mysql.connector
from utils.mensajes import mensajes 
from utils.rutas.rutas import obtener_ruta_recurso
import sys
import os
import logging
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')



def esperar_conexion():
    bandera_conexion = True
    while bandera_conexion:
        try:
            conexion = obtener_conexion()
            conexion.ping(reconnect=True)
            mensajes.mensajes_informacion("✅ Conexión a la base de datos exitosa.")
            return conexion
        except mysql.connector.Error as err:
            res = mensajes.mensajes_askyesno(f"⛔ Error al conectar a la base de datos: {err}\n¿Desea reintentar?")
            if res:
                mensajes.mensajes_Error(f"⛔ Error al conectar a la base de datos: {err}")
                mensajes.mensajes_Error("🔄 Reintentando conexión en 5 segundos...")
                time.sleep(5)
            else:
                mensajes.mensajes_informacion("🚪 Saliendo de la aplicación...")
                sys.exit()  # <-- Termina todo inmediatamente

 

def main():
    try:
        # Espera hasta que haya conexión
        conexion = esperar_conexion()
        logo_path = obtener_ruta_recurso("app/utils/images/logo.jpg")


        # Si llega aquí, ya hay conexión
        app = AppBase(
            rol="Administrador",
            logo_path=logo_path
        )

        app.mainloop()

    except FileNotFoundError as e:
        mensajes.mensajes_Error(f"⚠️ Archivo no encontrado: {e}")
        messagebox.showerror("Error", f"Archivo no encontrado:\n{e}")

    except tk.TclError as e:
        mensajes.mensajes_Error(f"❌ Error en la interfaz gráfica: {e}")
        messagebox.showerror("Error de interfaz", f"Ocurrió un error con la interfaz:\n{e}")

    except Exception as e:
        mensajes.mensajes_Error(f"❗ Error inesperado: {e}")
        logging.error("Error inesperado", exc_info=True)
        traceback.print_exc()
        messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")


if __name__ == "__main__":
    main()
