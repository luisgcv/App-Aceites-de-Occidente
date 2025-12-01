from config.settings import obtener_conexion

class Identificacion(): 
    def __init__(self):
        pass

    def obtener_identificaciones(self): 
        consulta = "SELECT * FROM vw_identificacion_detalle"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_identificacion(self,id_identificacion, valor,tipo_identificacion_id,nacionalidad_id,party_id): 
        consulta = "CALL sp_Actualizar_Identificacion   (%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(id_identificacion,valor,tipo_identificacion_id,nacionalidad_id,party_id))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_identificacion(self,valor,tipo_identificacion_id,nacionalidad_id,party_id): 
        consulta = "CALL sp_Insertar_Identificacion(%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(valor,tipo_identificacion_id, nacionalidad_id, party_id))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_identificacion(self,identificacion_id): 
        consulta = "CALL sp_Eliminar_Identificacion(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(identificacion_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        

        
    def buscar_identificacion(self,nombre): 
        consulta = "CALL sp_Buscar_Identificacion_PorNombre(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(nombre,))
            resultados = cursor.fetchall()
            print(resultados)
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return resultados

        except Exception as e: 
            return str(e)
        
        
    def filtrar_por_tipo_y_nombre(self, tipo, nombre): 
        consulta = "CALL sp_Filtrar_Identificacion_por_Tipo_y_Nombre(%s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (tipo, nombre))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
            
    def filtrar_por_tipo(self, tipo, nombre): 
        consulta = "CALL sp_Filtrar_Identificacion_por_Tipo(%s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (tipo, nombre))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)


    

