from config.settings import obtener_conexion


class TipoMecanismoContacto:
    """Acceso a la tabla tipo_mecanismo_contacto (CRUD completo)."""

    def __init__(self):
        pass

    # ──────────────────────────────── CONSULTAR ────────────────────────────────
    def obtener_tipos(self):
        consulta = "SELECT * FROM v_tipo_medio_contacto"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            conexion.close()
            return resultados
        except Exception as e:
            return str(e)

    # ──────────────────────────────── INSERTAR ────────────────────────────────
    def insertar_tipo(self, descripcion):
        consulta = "CALL sp_Insertar_Tipo_Medio_Contacto(%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (descripcion,))
            conexion.commit()
            while cursor.nextset():  # limpiar más resultados
                pass
            conexion.close()
            return True
        except Exception as e:
            return str(e)

    # ──────────────────────────────── ACTUALIZAR ───────────────────────────────
    def actualizar_tipo(self, tipo_id, descripcion):
        consulta = "CALL sp_Actualizar_Tipo_Medio_Contacto(%s, %s)"
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

    # ──────────────────────────────── ELIMINAR ────────────────────────────────
    def eliminar_tipo(self, tipo_id):
        consulta = "CALL sp_Eliminar_Tipo_Me canismo_Contacto(%s)"
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(consulta, (tipo_id,))
            # >>> Consumir el primer result‑set (SELECT ROW_COUNT)
            cursor.fetchall()
            # >>> Limpiar cualquier otro result‑set
            while cursor.nextset():
                cursor.fetchall()
            conexion.commit()
            conexion.close()
            return True
        except Exception as e:
            return str(e)


    # ──────────────────────────────── OBTENER ID POR DESCRIPCIÓN ──────────────
    def obtener_tipo_id(self, descripcion):
        """
        Devuelve el ID correspondiente a la descripción.
        Retorna None si no existe.
        """
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "CALL obtener_tipo_mecanismo_contacto_id(%s, @id)", (descripcion,)
            )
            cursor.execute("SELECT @id")
            resultado = cursor.fetchone()
            conexion.close()
            return resultado[0] if resultado and resultado[0] is not None else None
        except Exception as e:
            return str(e)
