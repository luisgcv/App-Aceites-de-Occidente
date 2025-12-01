from config.settings import obtener_conexion

class Party(): 
    def __init__(self):
        pass

    def obtener_personas(self): 
        consulta = "SELECT * FROM v_party"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def obtener_party_id(self, nombre):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("CALL obtener_party_id(%s, @id)", (nombre,))
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
        
        
    def insertar_persona(self, nombre, id_naturaleza): 
        consulta = "CALL sp_Insertar_Party(%s, %s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nombre, id_naturaleza))

            # Leer resultado con el party_id
            resultado = cursor.fetchone()
            party_id = resultado[0] if resultado else None

            # Asegura avanzar cualquier resultado adicional
            while cursor.nextset():
                pass

            conexion.commit()
            cursor.close()
            conexion.close()
            
            return party_id  # ← Devuelve el party_id

        except Exception as e: 
            return str(e)

        

    def eliminar_persona(self,persona_id): 
        consulta = "CALL sp_Eliminar_Party(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(persona_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        
    def actualizar_persona(self,persona_id,nombre,naturaleza_id): 
        consulta = "CALL sp_Actualizar_Party(%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(persona_id,nombre,naturaleza_id))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        
    def buscar_persona(self,nombre): 
        consulta = "CALL sp_Buscar_Party_PorNombre(%s)"

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
        
        
    def filtro_naturaleza(self, naturaleza): 
        consulta = "CALL sp_Filtrar_Party_PorNaturaleza(%s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(naturaleza,))
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        

     

