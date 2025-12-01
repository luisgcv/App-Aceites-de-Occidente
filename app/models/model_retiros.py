from config.settings import obtener_conexion

class Retiro(): 
    def __init__(self):
        pass

    def obtener_retiro(self): 
        consulta = "SELECT * FROM vw_retiro_detalle ORDER BY fecha DESC LIMIT 25;"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_retiro(self,retiro_id,descripcion,monto ,fecha ,empleado_id,banco_id): 
        consulta = "CALL sp_Actualizar_Retiro (%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(retiro_id,descripcion,monto ,fecha ,empleado_id,banco_id))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_retiro(self,descripcion,monto ,fecha ,empleado_id,banco_id): 
        consulta = "CALL sp_Insertar_Retiro(%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(descripcion,monto ,fecha ,empleado_id,banco_id))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_retiro(self,retiro_id): 
        consulta = "CALL sp_Eliminar_Retiro (%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(retiro_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        

        
            
    def filtrar_retiro(self, fecha_inicio, fecha_fin,empleado): 
        consulta = "CALL sp_Filtrar_Retiros(%s, %s,%s)"
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


    
