from models.model_transaccion import Transaccion
from controllers import controlador_banco

from utils.mensajes import mensajes


transaccion  = Transaccion()

def mostrar_transaccion():

    resultados = transaccion.obtener_transaccion()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados



def guardar_transaccion(banco_destino,banco_origen,monto, fecha, comprobante):
    if not banco_origen: 
        mensajes.mensajes_Error("Debe ingresar un banco origen ")
        return 
    if not banco_destino: 
        mensajes.mensajes_Error("Debe ingresar un banco destino ")
        return 

    if not monto: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return
    if not comprobante: 
        comprobante = None

    banco_id_origen = controlador_banco.obtener_banco_id(banco_origen) 
    banco_id_destino = controlador_banco.obtener_banco_id(banco_destino)

    if banco_id_origen is None:
        mensajes.mensajes_Error("Banco origen no encontrada en la base de datos")
        return
    if isinstance(banco_id_origen, str):
        mensajes.mensajes_Error(f"Error al obtener al banco origen : {banco_id_origen}")
        return  
    
    if banco_id_destino is None:
        mensajes.mensajes_Error("Banco destino no encontrada en la base de datos")
        return
    if isinstance(banco_id_destino, str):
        mensajes.mensajes_Error(f"Error al obtener al banco destino : {banco_id_destino}")
        return  



    accion = transaccion.insertar_transaccion( banco_id_destino,banco_id_origen,monto,fecha,comprobante)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_transaccion(transaccion_id): 
    if not transaccion_id: 
        mensajes.mensajes_Error("Debe seleccionar una transaccion ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar la transaccion con id: {transaccion_id}?")

    if not respuesta:
        return

    accion = transaccion.eliminar_transaccion(transaccion_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar la transaccion con id {transaccion_id}")


def actualizar_transaccion(transaccion_id,banco_destino,banco_origen,monto, fecha, comprobante):
    if not transaccion_id: 
        mensajes.mensajes_Error("Debe seleccionar una transaccion ")
        return 
    if not banco_origen: 
        mensajes.mensajes_Error("Debe ingresar un banco origen ")
        return 
    if not banco_destino: 
        mensajes.mensajes_Error("Debe ingresar un banco destino ")
        return 

    if not monto: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar una fecha")
        return
    if not comprobante: 
        comprobante = None

    banco_id_origen = controlador_banco.obtener_banco_id(banco_origen) 
    banco_id_destino = controlador_banco.obtener_banco_id(banco_destino)

    if banco_id_origen is None:
        mensajes.mensajes_Error("Banco origen no encontrada en la base de datos")
        return
    if isinstance(banco_id_origen, str):
        mensajes.mensajes_Error(f"Error al obtener al banco origen : {banco_id_origen}")
        return  
    
    if banco_id_destino is None:
        mensajes.mensajes_Error("Banco destino no encontrada en la base de datos")
        return
    if isinstance(banco_id_destino, str):
        mensajes.mensajes_Error(f"Error al obtener al banco destino : {banco_id_destino}")
        return  



    accion = transaccion.actualizar_transaccion(transaccion_id,banco_id_destino,banco_id_origen,monto,fecha,comprobante)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en actualizar")



def filtrar_transaccion(fecha_inicio, fecha_fin): 
    if not fecha_inicio:
        mensajes.mensajes_Error("Debe ingresar una fecha de inicio")
        return
    if not fecha_fin:
        mensajes.mensajes_Error("Debe ingresar una fecha de fin")
        return
    
    resultados = transaccion.filtrar_transaccion_fecha(fecha_inicio,fecha_fin)

    if isinstance(resultados, str):  # error como string
        mensajes.mensajes_informacion(f"Error: {resultados}")
        return 
    return resultados
