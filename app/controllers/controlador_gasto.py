from models.modelo_gasto import Gasto
from controllers import  controlador_empleado,controlador_metodo_pago,controlador_banco

from utils.mensajes import mensajes


gasto  = Gasto()

def mostrar_gasto():
    resultados = gasto.obtener_gasto()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados



def guardar_gasto(fecha,monto,metodo_pago,descripcion,imagen, empleado,banco):
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return 
    if not monto: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not metodo_pago: 
        mensajes.mensajes_Error("Debe ingresar un metodo de pago")
        return

    if not descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return
    if not imagen: 
        imagen = None
    if not empleado: 
        mensajes.mensajes_Error("Debe ingresar un empleado")
        return
    # Banco opcional
    banco_id = None
    if banco: 
        banco_id = controlador_banco.obtener_banco_id(banco) 
        if banco_id is None:
            mensajes.mensajes_Error("Banco no encontrado en la base de datos")
            return
        if isinstance(banco_id, str):
            mensajes.mensajes_Error(f"Error al obtener el banco: {banco_id}")
            return  



    # Obtener dinámicamente el ID de la naturaleza
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)
    metodo_pago_id = controlador_metodo_pago.obtener_metodo_pago_id(metodo_pago)

    # Validar si el ID fue encontrado correctamente 
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrada en la base de datos")
        return
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener al empleado: {empleado_id}")
        return   
    
    # Validar si el ID fue encontrado correctamente 
    if metodo_pago_id is None:
        mensajes.mensajes_Error("MEtodo de pago no encontrada en la base de datos")
        return
    if isinstance(metodo_pago_id, str):
        mensajes.mensajes_Error(f"Error al obtener el metodo de pago: {metodo_pago_id}")
        return   



    accion = gasto.insertar_gasto(fecha,monto,metodo_pago_id,descripcion,imagen,empleado_id,banco_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_gasto(gasto_id): 
    if not gasto_id: 
        mensajes.mensajes_Error("Debe seleccionar un gasto ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el gasto con id: {gasto_id}?")

    if not respuesta:
        return

    accion = gasto.eliminar_gasto(gasto_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar el gasto con id {gasto_id}")

def actualizar_gasto(gasto_id,fecha,monto,metodo_pago,descripcion,imagen, empleado,banco):
    if not gasto_id: 
        mensajes.mensajes_Error("Debe seleccionar un gasto")
        return      
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return 
    if not monto: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not metodo_pago: 
        mensajes.mensajes_Error("Debe ingresar un metodo de pago")
        return

    if not descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return
    if not imagen: 
        imagen = None
    if not empleado: 
        mensajes.mensajes_Error("Debe ingresar un empleado")
        return
    # Banco opcional
    banco_id = None
    if banco: 
        banco_id = controlador_banco.obtener_banco_id(banco) 
        if banco_id is None:
            mensajes.mensajes_Error("Banco no encontrado en la base de datos")
            return
        if isinstance(banco_id, str):
            mensajes.mensajes_Error(f"Error al obtener el banco: {banco_id}")
            return  

    # Obtener dinámicamente el ID de la naturaleza
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)
    metodo_pago_id = controlador_metodo_pago.obtener_metodo_pago_id(metodo_pago)

    # Validar si el ID fue encontrado correctamente 
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrada en la base de datos")
        return
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener al empleado: {empleado_id}")
        return   
    
    # Validar si el ID fue encontrado correctamente 
    if metodo_pago_id is None:
        mensajes.mensajes_Error("MEtodo de pago no encontrada en la base de datos")
        return
    if isinstance(metodo_pago_id, str):
        mensajes.mensajes_Error(f"Error al obtener el metodo de pago: {metodo_pago_id}")
        return   



    accion = gasto.actualizar_gasto(gasto_id,fecha,monto,metodo_pago_id,descripcion,imagen,empleado_id,banco_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la actualizacion")


def filtrar_gasto_fecha_empleado(fecha_inicio, fecha_fin, empleado):
    # Validar que al menos un filtro sea proporcionado
    if not fecha_inicio and not fecha_fin and not empleado:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro (rango de fechas o empleado).")
        return []

    # Validación adicional: si se proporciona solo una de las fechas, mostrar error
    if (fecha_inicio and not fecha_fin) or (fecha_fin and not fecha_inicio):
        mensajes.mensajes_Error("Debe ingresar ambas fechas: inicio y fin.")
        return []

    # Normalizar los valores
    empleado = empleado if empleado else None
    fecha_inicio = fecha_inicio if fecha_inicio else None
    fecha_fin = fecha_fin if fecha_fin else None

    try:
        resultado = gasto.filtrar_gasto_factura(fecha_inicio, fecha_fin, empleado)
        return resultado

    except Exception as e:
        mensajes.mensajes_Error(f"Ocurrió un error al filtrar: {e}")
        return []

