
from config.settings import obtener_conexion

class Reportes(): 
    def __init__(self):
        pass

    def obtener_total_ingresos_mes(self): 
            consulta = "SELECT * FROM vista_total_ingresos_mes"
            try: 
                conexion = obtener_conexion()
                cursor = conexion.cursor()
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                conexion.close()
                return resultados
            except Exception as e: 
                return str(e)
            
    def obtener_total_gasto_mes(self): 
        consulta = "SELECT * FROM vista_total_gastos_mes"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
                    
    def obtener_total_factura_mes(self): 
        consulta = "SELECT * FROM vista_total_facturas_mes"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
            
    def obtener_total_factura_estado_mes(self): 
        consulta = "SELECT * FROM vista_totales_facturas_estado_mes"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e) 
            
    def obtener_total_retiros_mes(self): 
        consulta = "SELECT * FROM vista_total_retiros_mes"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e) 
        
    def obtener_total_transacciones_mes(self): 
        consulta = "SELECT * FROM vista_total_transacciones_mes"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e) 
        

    def obtener_total_balance_mes(self): 
        consulta = "SELECT * FROM vista_balance_mes"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e) 
        
    def obtener_ganancia_neta(self,fecha_inicio,fecha_fin): 
        consulta = "CALL sp_Reporte_Ganancia_Neta_Rango(%s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        


    def obtener_salario_empleado(self, nombre, fecha_inicio, fecha_fin): 
        consulta = "CALL sp_Obtener_Salario_Empleado_PorNombreYRango(%s, %s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nombre,fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
