from config.settings import obtener_conexion

class Estado_Cuenta(): 
    def __init__(self):
        pass

    def obtener_estado_cuenta(self): 
        consulta = "SELECT * FROM vw_estado_cuenta_detalle ORDER BY fecha_inicio DESC LIMIT 25;"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_estado_cuenta(self,estado_cuenta_id,banco_id,p_fecha_inicio ,p_fecha_fin ,documento): 
        consulta = "CALL sp_Actualizar_Estado_Cuenta (%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(estado_cuenta_id,banco_id,p_fecha_inicio ,p_fecha_fin ,documento))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_estado_cuenta(self,banco_id,p_fecha_inicio ,p_fecha_fin ,documento): 
        consulta = "CALL sp_Insertar_Estado_Cuenta(%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(banco_id,p_fecha_inicio ,p_fecha_fin ,documento))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_estado_cuenta(self,estado_cuenta_id): 
        consulta = "CALL sp_Eliminar_Estado_Cuenta(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(estado_cuenta_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        

        
            
    def filtrar_fecha(self, fecha_inicio, fecha_fin): 
        consulta = "CALL sp_Filtrar_EstadoCuenta_PorFechas(%s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (fecha_inicio, fecha_fin ))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)


    

