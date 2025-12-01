from config.settings import obtener_conexion

class Factura(): 
    def __init__(self):
        pass

    def obtener_factura(self): 
        consulta = "SELECT * FROM vw_factura_detalle ORDER BY fecha DESC LIMIT 25"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def obtener_numero_factura(self): 
        consulta = "SELECT * FROM vista_factura_id_numero"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
        
    def actualizar_factura(self,factura_id, cliente_id,fecha,numero_factura,pagada,documento_pdf,monto): 
        consulta = "CALL sp_Actualizar_Factura (%s,%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(factura_id, cliente_id,fecha,numero_factura,pagada,documento_pdf,monto))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def marcar_factura_pagada(self,factura_id, estado): 
        consulta = "CALL sp_Marcar_Factura_Por_Estado(%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(factura_id,estado))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_factura(self,cliente_id,fecha,numero_factura,pagada,documento_pdf,monto): 
        consulta = "CALL sp_Insertar_Factura(%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(cliente_id,fecha,numero_factura,pagada,documento_pdf,monto))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_factura(self,factura_id): 
        consulta = "CALL sp_Eliminar_Factura(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(factura_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        


        
            
    def filtrar_facturas(self, fecha_inicio, fecha_fin): 
        consulta = "CALL sp_Filtrar_Factura_Por_Fecha(%s, %s)"
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
        
    def filtrar_facturas_nombre_pagada(self, nombre, pagada): 
        consulta = "CALL sp_Filtrar_Facturas(%s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nombre, pagada))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)



    
    def obtener_factura_id(self, numero_factura):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("CALL sp_Obtener_Id_Factura(%s, @id)", (numero_factura,))
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
        

