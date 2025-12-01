from config.settings import obtener_conexion

class Inicio(): 
    def __init__(self):
        pass

    def obtener_factura_pendiente(self): 
        consulta = "SELECT * FROM vista_facturas_pendientes "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def obtener_total_gastos_mes(self): 
        consulta = "SELECT * FROM vista_gastos_mensuales  "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def obtener_ingresos_mensuales(self): 
        consulta = "SELECT * FROM vista_ingresos_mensuales  "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)

        
    def obtener_ultimos_gastos(self): 
        consulta = "SELECT * FROM vista_ultimos_gastos   "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    

    def obtener_transacciones_recientes(self): 
        consulta = "SELECT * FROM vista_transacciones_recientes    "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)

    def obtener_factura_estado(self): 
        consulta = "SELECT * FROM vista_facturas_estado    "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def obtener_retiros_recientes(self): 
        consulta = "SELECT * FROM vista_retiros_recientes"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        

        
