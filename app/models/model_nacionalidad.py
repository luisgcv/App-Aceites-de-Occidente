from config.settings import obtener_conexion

class Nacionalidad:
    def __init__(self):
        pass

    def obtener_nacionalidades(self):
        consulta = "SELECT * FROM v_nacionalidad"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e:
            return str(e)

    def insertar_nacionalidad(self, descripcion):
        consulta = "CALL sp_Insertar_Nacionalidad(%s)"
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

    def actualizar_nacionalidad(self, nacionalidad_id, descripcion):
        consulta = "CALL sp_Actualizar_Nacionalidad(%s, %s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nacionalidad_id, descripcion))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def eliminar_nacionalidad(self, nacionalidad_id):
        consulta = "CALL sp_Eliminar_Nacionalidad(%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (nacionalidad_id,))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def obtener_nacionalidad_id(self, descripcion):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("CALL obtener_nacionalidad_id(%s, @id)", (descripcion,))
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
