from config.settings import obtener_conexion

class RelacionPuesto(): 
    def __init__(self):
        pass

    def obtener_relacion(self): 
        consulta = "SELECT * FROM vw_relacion_puesto_trabajo_detalle"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
    def actualizar_relacion(self,p_id_relacion , p_empleado_id,p_puesto_id ,p_descripcion): 
        consulta = "CALL sp_Actualizar_Relacion_Puesto  (%s,%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(p_id_relacion ,p_empleado_id,p_puesto_id ,p_descripcion))
            conexion.commit()
            conexion.close()
            
            return True 
        except Exception as e: 
            return str(e)
        
    def insertar_relacion(self,p_empleado_id ,p_puesto_id ,p_descripcion ): 
        consulta = "CALL sp_Insertar_Relacion_Puesto_Trabajo (%s,%s,%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(p_empleado_id ,p_puesto_id ,p_descripcion))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
        
            return True

        except Exception as e: 
            return str(e)
        

    def eliminar_relacion(self,relacion_id): 
        consulta = "CALL sp_Eliminar_Relacion_Puesto (%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(relacion_id,))
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return True

        except Exception as e: 
            return str(e)
        

        
    def buscar_relacion(self,nombre_completo): 
        consulta = "CALL sp_BuscarRelacionPorNombreCompleto (%s)"

        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta,(nombre_completo,))
            resultados = cursor.fetchall()
            print(resultados)
            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return resultados

        except Exception as e: 
            return str(e)
        
        
    def filtrar_por_nombre_puesto(self, nombre, puesto): 
        consulta = "CALL sp_FiltrarRelacion(%s, %s)"
        try: 
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nombre, puesto))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.close()
            return resultados
        except Exception as e: 
            return str(e)
        
            



    

