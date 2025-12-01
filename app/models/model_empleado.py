from config.settings import obtener_conexion

class Empleado:
    def __init__(self):
        pass

    def obtener_empleados(self):
        consulta = "SELECT * FROM v_empleado"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e:
            return str(e)
        
    def obtener_nombre_completo(self):
        consulta = "SELECT * FROM vista_empleados_nombre_completo "
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e:
            return str(e)

    def insertar_empleado(self, primer_apellido,segundo_apellido,fecha_nacimiento,party_id):
        consulta = "CALL sp_Insertar_Empleado(%s,%s,%s,%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (primer_apellido,segundo_apellido,fecha_nacimiento,party_id))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def actualizar_empleado(self,empleado_id,primer_apellido,segundo_apellido,fecha_nacimiento,party_id):
        consulta = "CALL sp_Actualizar_Empleado(%s, %s,%s,%s,%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (empleado_id,primer_apellido,segundo_apellido,fecha_nacimiento,party_id))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def eliminar_empleado(self, empleado_id):
        consulta = "CALL sp_Eliminar_Empleado(%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (empleado_id,))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def obtener_empleado_id(self, nombre_completo):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("CALL ObtenerEmpleadoIDPorNombreCompleto(%s, @id)", (nombre_completo,))
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
        
    def buscar_empleado_por_nombre_completo(self, nombre_completo):
        consulta = "CALL sp_Buscar_Empleado_Por_NombreCompleto(%s)"

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nombre_completo,))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return resultados

        except Exception as e:
            return str(e)


    def buscar_empleado_por_apellidos(self, primer_apellido, segundo_apellido):
        consulta = "CALL sp_Buscar_Empleado_Por_Apellidos(%s, %s)"

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (primer_apellido, segundo_apellido))
            resultados = cursor.fetchall()

            while cursor.nextset():
                pass

            conexion.commit()
            conexion.close()
            return resultados

        except Exception as e:
            return str(e)
