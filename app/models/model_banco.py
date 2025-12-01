from config.settings import obtener_conexion

class Banco(): 
    def __init__(self):
        pass

    def obtener_banco(self): 
        consulta = "SELECT * FROM v_banco"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def obtener_cuenta_iban(self): 
        consulta = "SELECT * FROM vista_cuentas_iban"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_banco(self,banco_id, nombre_banco,cuenta_iban,cuenta_cliente,party_id): 
        consulta = "CALL sp_Actualizar_Banco (%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(banco_id, nombre_banco,cuenta_iban,cuenta_cliente,party_id))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_banco(self,nombre_banco,cuenta_iban,cuenta_cliente,party_id): 
        consulta = "CALL sp_Insertar_Banco(%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(nombre_banco,cuenta_iban,cuenta_cliente,party_id))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_banco(self,banco_id): 
        consulta = "CALL sp_eliminar_banco(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(banco_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        
    
            
    def filtrar_bancos(self, nombre_banco, party_nombre): 
        consulta = "CALL sp_filtrar_bancos(%s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nombre_banco, party_nombre))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)


    
    def obtener_banco_id(self, cuenta):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("CALL sp_Obtener_Banco_Id_PorIban(%s, @id)", (cuenta,))
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
