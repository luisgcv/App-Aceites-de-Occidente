from config.settings import obtener_conexion

class Gasto(): 
    def __init__(self):
        pass

    def obtener_gasto(self): 
        consulta = "SELECT * FROM vw_gasto_detalle ORDER BY fecha DESC LIMIT 25; "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        

        
    def actualizar_gasto(self,gasto_id,fecha,monto,metodo_pago_id,descripcion,imagen, empleado_id,banco_id): 
        consulta = "CALL sp_Actualizar_Gasto (%s,%s,%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(gasto_id,fecha,monto,metodo_pago_id,descripcion,imagen, empleado_id,banco_id))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        

        
    def insertar_gasto(self,fecha,monto,metodo_pago_id,descripcion,imagen, empleado_id,banco_id): 
        consulta = "CALL sp_Insertar_Gasto(%s,%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(fecha,monto,metodo_pago_id,descripcion,imagen, empleado_id,banco_id))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_gasto(self,gasto_id): 
        consulta = "CALL sp_Eliminar_Gasto(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(gasto_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        
            
    def filtrar_gasto_factura(self, fecha_inicio, fecha_fin,empleado): 
        consulta = "CALL sp_Filtrar_Gastos(%s, %s,%s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (fecha_inicio, fecha_fin,empleado))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        