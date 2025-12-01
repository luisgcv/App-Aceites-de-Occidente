from models.model_factura import Factura
from controllers import  controlador_party

from utils.mensajes import mensajes


factura  = Factura()

def mostrar_factura():
    resultados = factura.obtener_factura()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados

def mostrar_numero_factura():
    resultados = factura.obtener_numero_factura()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def guardar_factura(cliente,fecha,numero_factura,documento_pdf,monto):
    if not cliente: 
        mensajes.mensajes_Error("Debe ingresar un cliente")
        return 
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return
    if not numero_factura: 
        mensajes.mensajes_Error("Debe ingresar un numero de factura")
        return

    if not documento_pdf: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    
    pagada = 0

    # Obtener dinámicamente el ID de la naturaleza
    cliente_id = controlador_party.obtener_party_id(cliente)

    # Validar si el ID fue encontrado correctamente 
    if cliente_id is None:
        mensajes.mensajes_Error("Cliente no encontrada en la base de datos")
        return
    if isinstance(cliente_id, str):
        mensajes.mensajes_Error(f"Error al obtener al cliente: {cliente_id}")
        return   

    accion = factura.insertar_factura(cliente_id,fecha,numero_factura,pagada,documento_pdf,monto)
    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_factura(factura_id): 
    if not factura_id: 
        mensajes.mensajes_Error("Debe seleccionar una factura ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el banco con id: {factura_id}?")

    if not respuesta:
        return

    accion = factura.eliminar_factura(factura_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar la factura con id {factura_id}")


def actualizar_factura(factura_id,cliente,fecha,numero_factura,documento_pdf,monto):
    if not factura_id: 
        mensajes.mensajes_Error("Debe seleccionar una factura")
        return 
    if not cliente: 
        mensajes.mensajes_Error("Debe ingresar un cliente")
        return 
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return
    if not numero_factura: 
        mensajes.mensajes_Error("Debe ingresar un numero de factura")
        return

    if not documento_pdf: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return


    # Obtener dinámicamente el ID de la naturaleza
    cliente_id = controlador_party.obtener_party_id(cliente)

    # Validar si el ID fue encontrado correctamente 
    if cliente_id is None:
        mensajes.mensajes_Error("Cliente no encontrada en la base de datos")
        return
    if isinstance(cliente_id, str):
        mensajes.mensajes_Error(f"Error al obtener al cliente: {cliente_id}")
        return   
    
    pagada = 0

    accion = factura.actualizar_factura(factura_id,cliente_id,fecha,numero_factura,pagada,documento_pdf,monto)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la actualización")


def filtrar_factura_fecha(fecha_inicio, fecha_fin):

    # Validar que al menos uno tenga valor
    if not fecha_fin and not fecha_inicio:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro.")
        return []
    
    resultado = factura.filtrar_facturas(fecha_inicio, fecha_fin)

    if isinstance(resultado, str):  # error como string
        mensajes.mensajes_Error(f"Error: {resultado}")
        return

    return resultado

def filtrar_factura_nombre_pagadas(nombre, pagada):
    # Validar que al menos uno tenga valor válido (no vacío ni None)
    if not nombre and pagada is None:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro (nombre o pagada).")
        return []

    # Normalizar los valores para enviar al modelo
    nombre = nombre if nombre else None
    pagada = pagada if pagada in (0, 1) else None

    try:
        resultado = factura.filtrar_facturas_nombre_pagada(nombre, pagada)
        return resultado

    except Exception as e:
        mensajes.mensajes_Error(f"Ocurrió un error al filtrar: {e}")
        return []

def marcar_factura(factura_id,pagada): 
    return factura.marcar_factura_pagada(factura_id,pagada)


def obtener_factura_id(numero_factura):
    return factura.obtener_factura_id(numero_factura)