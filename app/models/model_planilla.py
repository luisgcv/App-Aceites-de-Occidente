from config.settings import obtener_conexion

class Planilla(): 
    def __init__(self):
        pass

    def obtener_planilla(self): 
        consulta = "SELECT * FROM vw_planilla_detalle ORDER BY fecha_inicio DESC LIMIT 25; "
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_planilla(self,planilla_id, empleado_id,fecha_inicio,fecha_fin,horas_trabajadas,pago_por_hora,salario, comentarios): 
        consulta = "CALL sp_Actualizar_Planilla(%s,%s,%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(planilla_id, empleado_id,fecha_inicio,fecha_fin,horas_trabajadas,pago_por_hora,salario, comentarios))
            conexion.commit()
            conexion.close()
            afectadas = cursor.rowcount
            return True if afectadas > 0 else False 

        except Exception as e: 
            return str(e)
        
    def insertar_planilla(self,empleado_id,fecha_inicio,fecha_fin,horas_trabajadas,pago_por_hora,salario, comentarios): 
        consulta = "CALL sp_Insertar_Planilla(%s,%s,%s,%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(empleado_id,fecha_inicio,fecha_fin,horas_trabajadas,pago_por_hora,salario, comentarios))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_planilla(self,planilla_id): 
        consulta = "CALL sp_eliminar_planilla(%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(planilla_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        


            
    def filtrar_planilla_fecha(self, fecha_inicio, fecha_fin): 
        consulta = "CALL sp_Filtrar_Planilla_Por_Fecha(%s, %s)"
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


    

