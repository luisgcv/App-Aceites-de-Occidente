from models.model_tipo_identificacion import TipoIdentificacion
from utils.mensajes import mensajes

tipo_identificacion_model = TipoIdentificacion()

def guardar_tipo_identificacion(descripcion):
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = tipo_identificacion_model.insertar_tipo(descripcion)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_tipo_identificacion(tipo_identificacion_id):
    if not tipo_identificacion_id:
        mensajes.mensajes_Error("Debe seleccionar un tipo de identificación")
        return

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el tipo de identificación con id: {tipo_identificacion_id}?")
    if not respuesta:
        return

    accion = tipo_identificacion_model.eliminar_tipo(tipo_identificacion_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito al eliminar el tipo de identificación con id {tipo_identificacion_id}")


def mostrar_tipos_identificacion():
    resultados = tipo_identificacion_model.obtener_tipos()

    if isinstance(resultados, str):
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:
        return None

    return resultados


def actualizar_tipo_identificacion(tipo_identificacion_id, descripcion):
    if not tipo_identificacion_id:
        mensajes.mensajes_Error("Debe seleccionar un tipo de identificación de la tabla")
        return
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    accion = tipo_identificacion_model.actualizar_tipo(tipo_identificacion_id, descripcion)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito al actualizar a '{descripcion}'")


def obtener_tipo_identificacion_id(descripcion):
    return tipo_identificacion_model.obtener_tipo_id(descripcion)
