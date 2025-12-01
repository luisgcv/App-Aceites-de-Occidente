# controllers/controller_tipo_mecanismo_contacto.py
from models.model_tipo_mecanismo import TipoMecanismoContacto
from utils.mensajes import mensajes

tipo_mecanismo_model = TipoMecanismoContacto()

# ──────────────────────────── CREAR ────────────────────────────
def guardar_tipo_mecanismo(descripcion: str) -> None:
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = tipo_mecanismo_model.insertar_tipo(descripcion)

    if isinstance(accion, str):           # se devolvió un error como cadena
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


# ──────────────────────────── ELIMINAR ─────────────────────────
def eliminar_tipo_mecanismo(tipo_id: int) -> None:
    if not tipo_id:
        mensajes.mensajes_Error("Debe seleccionar un tipo de mecanismo de contacto")
        return

    respuesta = mensajes.mensajes_askyesno(
        f"¿Eliminar el tipo de mecanismo de contacto con id: {tipo_id}?"
    )
    if not respuesta:
        return

    accion = tipo_mecanismo_model.eliminar_tipo(tipo_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(
            f"Éxito al eliminar el tipo de mecanismo de contacto con id {tipo_id}"
        )


# ──────────────────────────── LISTAR ───────────────────────────
def mostrar_tipos_mecanismo():
    resultados = tipo_mecanismo_model.obtener_tipos()

    if isinstance(resultados, str):
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:
        return None

    return resultados


# ──────────────────────────── ACTUALIZAR ───────────────────────
def actualizar_tipo_mecanismo(tipo_id: int, descripcion: str) -> None:
    if not tipo_id:
        mensajes.mensajes_Error("Debe seleccionar un tipo de mecanismo de contacto de la tabla")
        return
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = tipo_mecanismo_model.actualizar_tipo(tipo_id, descripcion)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito al actualizar a '{descripcion}'")


# ──────────────────────────── OBTENER ID ───────────────────────
def obtener_tipo_mecanismo_id(descripcion: str):
    """
    Devuelve el ID asociada a la descripción,
    o None si no existe.
    """
    return tipo_mecanismo_model.obtener_tipo_id(descripcion)
