from config.settings import obtener_conexion

class PuestoTrabajo:
    def __init__(self):
        pass

    def obtener_puestos(self):
        consulta = "SELECT * FROM v_puesto"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e:
            return str(e)

    def insertar_puesto(self, descripcion):
        consulta = "CALL sp_Insertar_Puesto(%s)"
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

    def actualizar_puesto(self, puesto_id, descripcion):
        consulta = "CALL sp_Actualizar_Puesto(%s, %s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (puesto_id, descripcion))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def eliminar_puesto(self, puesto_id):
        consulta = "CALL sp_Eliminar_Puesto(%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (puesto_id,))
            conexion.commit()
            while cursor.nextset():
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    def obtener_puesto_id(self, descripcion):
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("CALL obtener_puesto_id(%s, @id)", (descripcion,))
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
