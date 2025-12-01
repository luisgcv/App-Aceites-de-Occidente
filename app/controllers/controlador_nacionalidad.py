from models.model_nacionalidad import Nacionalidad
from utils.mensajes import mensajes

nacionalidad_model = Nacionalidad()

def guardar_nacionalidad(descripcion):
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = nacionalidad_model.insertar_nacionalidad(descripcion)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_nacionalidad(nacionalidad_id):
    if not nacionalidad_id:
        mensajes.mensajes_Error("Debe seleccionar una nacionalidad")
        return

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar la nacionalidad con id: {nacionalidad_id}?")
    if not respuesta:
        return

    accion = nacionalidad_model.eliminar_nacionalidad(nacionalidad_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito en eliminar la nacionalidad con id {nacionalidad_id}")


def mostrar_nacionalidad():
    resultados = nacionalidad_model.obtener_nacionalidades()

    if isinstance(resultados, str):
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:
        return None

    return resultados


def actualizar_nacionalidad(nacionalidad_id, descripcion):
    if not nacionalidad_id:
        mensajes.mensajes_Error("Debe seleccionar una nacionalidad de la tabla")
        return
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = nacionalidad_model.actualizar_nacionalidad(nacionalidad_id, descripcion)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito al actualizar a '{descripcion}'")


def obtener_nacionalidad_id(descripcion):
    return nacionalidad_model.obtener_nacionalidad_id(descripcion)
