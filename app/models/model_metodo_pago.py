from config.settings import obtener_conexion


class MetodoPago:
    """Acceso CRUD para la tabla metodo_pago."""

    # ──────────────── LISTAR ────────────────
    def obtener_todos(self):
        consulta = "SELECT * FROM v_metodo_pago"      # crea la vista o cámbiala
        try:
            con = obtener_conexion()
            cur = con.cursor()
            cur.execute(consulta)
            rows = cur.fetchall()
            con.close()
            return rows
        except Exception as e:
            return str(e)

    # ──────────────── INSERTAR ───────────────
    def insertar(self, descripcion):
        consulta = "CALL sp_Insertar_Metodo_Pago(%s)"
        try:
            con = obtener_conexion()
            cur = con.cursor()
            cur.execute(consulta, (descripcion,))
            con.commit()
            while cur.nextset():
                pass
            con.close()
            return True
        except Exception as e:
            return str(e)

    # ──────────────── ACTUALIZAR ─────────────
    def actualizar(self, mp_id, descripcion):
        consulta = "CALL sp_Actualizar_Metodo_Pago(%s, %s)"
        try:
            con = obtener_conexion()
            cur = con.cursor()
            cur.execute(consulta, (mp_id, descripcion))
            con.commit()
            while cur.nextset():
                pass
            con.close()
            return True
        except Exception as e:
            return str(e)

    # ──────────────── ELIMINAR ───────────────
    def eliminar(self, mp_id):
        consulta = "CALL sp_Eliminar_Metodo_Pago(%s)"
        try:
            con = obtener_conexion()
            cur = con.cursor()
            cur.execute(consulta, (mp_id,))
            cur.fetchall()           # ← evita “Unread result”
            while cur.nextset():
                cur.fetchall()
            con.commit()
            con.close()
            return True
        except Exception as e:
            return str(e)

    # ──────────────── OBTENER ID ─────────────
    def obtener_id(self, descripcion):
        try:
            con = obtener_conexion()
            cur = con.cursor()
            cur.execute("CALL obtener_metodo_pago_id(%s, @id)", (descripcion,))
            cur.execute("SELECT @id")
            res = cur.fetchone()
            con.close()
            return res[0] if res and res[0] is not None else None
        except Exception as e:
            return str(e)
