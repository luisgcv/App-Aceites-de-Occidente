from config.settings import obtener_conexion

class MecanismoContacto(): 
    def __init__(self):
        pass

    def obtener_mecanismo_contacto(self): 
        consulta = "SELECT * FROM v_medio_contacto"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_medio_contacto(self,medio_contacto_id, valor,prioridad,tipo_id,party_id): 
        consulta = "CALL sp_Actualizar_Medio_Contacto   (%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(medio_contacto_id,valor,prioridad,tipo_id,party_id))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_medio_contacto(self,valor,prioridad,tipo_id,party_id): 
        consulta = "CALL sp_Insertar_Medio_Contacto(%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(valor,prioridad, tipo_id, party_id))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_medio_contacto(self,medio_contacto_id): 
        consulta = "CALL sp_Eliminar_Medio_Contacto(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(medio_contacto_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        

        
    def buscar_medio_contacto(self,nombre): 
        consulta = "CALL sp_Buscar_Medio_Contacto_PorNombre(%s)"

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
        consulta = "CALL sp_Filtrar_Medio_Contacto_por_Tipo_y_Nombre(%s, %s)"
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


    

