from models.model_metodo_pago import MetodoPago
from utils.mensajes import mensajes

mp_model = MetodoPago()

def guardar_metodo_pago(descripcion):
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return
    ok = mp_model.insertar(descripcion)
    if isinstance(ok, str):
        mensajes.mensajes_Error(f"Error: {ok}")
    elif ok:
        mensajes.mensajes_informacion("Método de pago insertado correctamente")

def eliminar_metodo_pago(mp_id):
    if not mp_id:
        mensajes.mensajes_Error("Seleccione un método de pago")
        return
    if not mensajes.mensajes_askyesno(f"¿Eliminar el método de pago con id {mp_id}?"):
        return
    ok = mp_model.eliminar(mp_id)
    if isinstance(ok, str):
        mensajes.mensajes_Error(f"Error: {ok}")
    elif ok:
        mensajes.mensajes_informacion("Método de pago eliminado")

def actualizar_metodo_pago(mp_id, descripcion):
    if not mp_id:
        mensajes.mensajes_Error("Seleccione un método de pago")
        return
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return
    ok = mp_model.actualizar(mp_id, descripcion)
    if isinstance(ok, str):
        mensajes.mensajes_Error(f"Error: {ok}")
    elif ok:
        mensajes.mensajes_informacion("Método de pago actualizado")

def mostrar_metodos_pago():
    datos = mp_model.obtener_todos()
    if isinstance(datos, str):
        mensajes.mensajes_Error(f"Error: {datos}")
        return None
    return datos

def obtener_metodo_pago_id(descripcion):
    return mp_model.obtener_id(descripcion)
