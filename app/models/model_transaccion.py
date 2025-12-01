from config.settings import obtener_conexion

class Transaccion(): 
    def __init__(self):
        pass

    def obtener_transaccion(self): 
        consulta = "SELECT * FROM v_transacciones ORDER BY fecha DESC LIMIT 25; "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        

        
    def actualizar_transaccion(self,transaccion_id, banco_Id_destino,banco_Id_origen,monto, fecha, comprobante): 
        consulta = "CALL sp_Actualizar_Transaccion (%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(transaccion_id, banco_Id_destino,banco_Id_origen,monto, fecha, comprobante))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        

        
    def insertar_transaccion(self, banco_Id_destino,banco_Id_origen,monto, fecha, comprobante): 
        consulta = "CALL sp_Insertar_Transaccion(%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(banco_Id_destino,banco_Id_origen,monto, fecha, comprobante))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_transaccion(self,transaccion_id): 
        consulta = "CALL sp_Eliminar_Transaccion(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(transaccion_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        
            
    def filtrar_transaccion_fecha(self,fecha_inicio, fecha_fin): 
        consulta = "CALL sp_Filtrar_Transacciones_PorFecha(%s, %s)"
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
        