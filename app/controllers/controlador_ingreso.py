from models.model_ingreso import Ingreso
from controllers import  controlador_factura

from utils.mensajes import mensajes


ingreso  = Ingreso()

def mostrar_factura():
    resultados = ingreso.obtener_ingreso()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    

    return resultados



def guardar_ingreso(factura, monto, fecha, descripcion):
    if not monto:
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not fecha:
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return
    if not descripcion:
        mensajes.mensajes_Error("Debe ingresar una descripción")
        return

    factura_id = None
    if factura:
        factura_id = controlador_factura.obtener_factura_id(factura)
        if factura_id is None:
            mensajes.mensajes_Error("Factura no encontrada en la base de datos")
            return
        if isinstance(factura_id, str):  # Si hubo un error
            mensajes.mensajes_Error(f"Error al obtener la factura: {factura_id}")
            return

    if factura_id: 
        controlador_factura.marcar_factura(factura_id,1)

    accion = ingreso.insertar_ingreso(factura_id, monto, fecha, descripcion)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")

def eliminar_factura(ingreso_id,num_factura): 
    if not ingreso_id: 
        mensajes.mensajes_Error("Debe seleccionar un ingreso ")
        return 
    



    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el ingreso con id: {ingreso_id}?")


    if not respuesta:
        return
    

    factura_id = None
    if num_factura:
        factura_id = controlador_factura.obtener_factura_id(num_factura)
        if factura_id is None:
            mensajes.mensajes_Error("Factura no encontrada en la base de datos")
            return
        if isinstance(factura_id, str):  # Si hubo un error
            mensajes.mensajes_Error(f"Error al obtener la factura: {factura_id}")
            return

    if factura_id: 
        controlador_factura.marcar_factura(factura_id,0)

    accion = ingreso.eliminar_ingreso(ingreso_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar el ingreso con id {ingreso_id}")

def actualizar_ingreso(ingreso_id,factura, monto,fecha,descripcion):
    if not ingreso_id: 
        mensajes.mensajes_Error("Debe seleccionar un ingreso ")
        return 
    if not monto: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return

    if not descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return
    
    factura_id = None
    if factura:
        factura_id = controlador_factura.obtener_factura_id(factura)
        if factura_id is None:
            mensajes.mensajes_Error("Factura no encontrada en la base de datos")
            return
        if isinstance(factura_id, str):  # Si hubo un error
            mensajes.mensajes_Error(f"Error al obtener la factura: {factura_id}")
            return
        

    accion = ingreso.actualizar_ingreso(ingreso_id,factura_id, monto,fecha,descripcion)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito")


def filtrar_ingreso(fecha_inicio, fecha_fin):

    # Validar que al menos uno tenga valor
    if not fecha_fin and not fecha_inicio:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro.")
        return []
    
    resultado = ingreso.filtrar_ingreso(fecha_inicio, fecha_fin)

    if isinstance(resultado, str):  # error como string
        mensajes.mensajes_Error(f"Error: {resultado}")
        return

    return resultado



