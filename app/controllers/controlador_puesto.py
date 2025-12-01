from models.model_puesto_trabajo import PuestoTrabajo
from utils.mensajes import mensajes

puesto_model = PuestoTrabajo()

def guardar_puesto(descripcion):
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = puesto_model.insertar_puesto(descripcion)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_puesto(puesto_id):
    if not puesto_id:
        mensajes.mensajes_Error("Debe seleccionar un puesto")
        return

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el puesto con id: {puesto_id}?")
    if not respuesta:
        return

    accion = puesto_model.eliminar_puesto(puesto_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito al eliminar el puesto con id {puesto_id}")


def mostrar_puestos():
    resultados = puesto_model.obtener_puestos()

    if isinstance(resultados, str):
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:
        return None

    return resultados


def actualizar_puesto(puesto_id, descripcion):
    if not puesto_id:
        mensajes.mensajes_Error("Debe seleccionar un puesto de la tabla")
        return
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = puesto_model.actualizar_puesto(puesto_id, descripcion)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito al actualizar a '{descripcion}'")


def obtener_puesto_id(descripcion):
    return puesto_model.obtener_puesto_id(descripcion)
