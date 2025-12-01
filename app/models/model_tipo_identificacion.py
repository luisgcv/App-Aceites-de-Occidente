from config.settings import obtener_conexion

class TipoIdentificacion:
    def __init__(self):
        pass

    def obtener_tipos(self):
        consulta = "SELECT * FROM v_tipo_identificacion"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e:
            return str(e)

    def insertar_tipo(self, descripcion):
        consulta = "CALL sp_Insertar_Tipo_Identificacion(%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (descripcion,))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def actualizar_tipo(self, tipo_id, descripcion):
        consulta = "CALL sp_Actualizar_Tipo_Identificacion(%s, %s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (tipo_id, descripcion))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def eliminar_tipo(self, tipo_id):
        consulta = "CALL sp_Eliminar_Tipo_Identificacion(%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (tipo_id,))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def obtener_tipo_id(self, descripcion):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("CALL obtener_tipo_identificacion_id(%s, @id)", (descripcion,))
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
