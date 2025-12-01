from config.settings import obtener_conexion

class Ingreso(): 
    def __init__(self):
        pass

    def obtener_ingreso(self): 
        consulta = "SELECT * FROM vw_ingreso_detalle ORDER BY fecha DESC LIMIT 25;"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()

            return resultados
        except Exception as e: 
            return str(e)
        

        
    def actualizar_ingreso(self,ingreso_id,factura_id, monto,fecha,descripcion): 
        consulta = "CALL sp_Actualizar_Ingreso (%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(ingreso_id,factura_id, monto,fecha,descripcion))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_ingreso(self,factura_id, monto,fecha,descripcion): 
        consulta = "CALL sp_Insertar_Ingreso(%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(factura_id, monto,fecha,descripcion))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_ingreso(self,ingreso_id): 
        consulta = "CALL sp_Eliminar_Ingreso(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(ingreso_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        


        
            
    def filtrar_ingreso(self, fecha_inicio, fecha_fin): 
        consulta = "CALL sp_Filtrar_Ingresos_PorFechas(%s, %s)"
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


    
