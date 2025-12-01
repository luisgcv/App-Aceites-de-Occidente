from config.settings import obtener_conexion

class Cliente(): 
    def __init__(self):
        pass

    def obtener_cliente(self): 
        consulta = "SELECT * FROM v_cliente"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def es_cliente(self, party_id):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Ejecutar el procedimiento con el parámetro IN y la variable OUT definida
            cursor.execute("CALL sp_es_cliente(%s, @es_cliente)", (party_id,))
            
            # Consumir resultados para liberar cursor
            while cursor.nextset():
                pass

            cursor.execute("SELECT @es_cliente")
            resultado = cursor.fetchone()
            conexion.close()

            if resultado and resultado[0] is not None:
                return bool(resultado[0])
            else:
                return False

        except Exception as e:
            return str(e)

        
        
    def insertar_cliente(self,party_id): 
        consulta = "CALL sp_Insertar_Cliente(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(party_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_cliente(self,party_id): 
        consulta = "CALL eliminar_cliente(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(party_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        
        