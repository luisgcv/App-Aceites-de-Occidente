from config.settings import obtener_conexion

class Naturaleza_Party(): 
    def __init__(self):
        pass

    def obtener_naturaleza(self): 
        consulta = "SELECT * FROM v_naturaleza_party"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_naturaleza(self,naturaleza_id,descripcion): 
        consulta = "CALL sp_Actualizar_Naturaleza_Party(%s,%s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(naturaleza_id,descripcion))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True 
        except Exception as e: 
            return str(e)
        
    def eliminar_naturaleza(self,id_naturaleza): 
        consulta = "CALL sp_Eliminar_Naturaleza_Party(%s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(id_naturaleza,))
            conexion.commit()
            while cursor.nextset():
                pass

            conexion.close()
            return True 
        
        except Exception as e: 
            return str(e)
        
    def inrgesar_naturaleza(self,descripcion): 
        consulta = "CALL sp_Insertar_Naturaleza_Party(%s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(descripcion,))
            conexion.commit()
            while cursor.nextset():
                pass

            conexion.close()
            return True 
        
        except Exception as e: 
            return str(e)

    

    def obtener_naturaleza_id(self, descripcion):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Llamar al procedimiento con el parámetro de entrada y la variable de salida
            cursor.execute("CALL obtener_naturaleza_id(%s, @id)", (descripcion,))
            
            # Recuperar el valor de salida
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()

            conexion.close()

            # resultado es una tupla como (1,) o (2,)
            if resultado and resultado[0] is not None:
                return resultado[0]
            else:
                return None  # o algún mensaje como "No encontrado"

        except Exception as e:
            return str(e)
