from models.model_estado_cuenta import Estado_Cuenta
from controllers import  controlador_banco

from utils.mensajes import mensajes


estado_cuenta  = Estado_Cuenta()

def mostrar_estado_cuenta():
    resultados = estado_cuenta.obtener_estado_cuenta()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    

    return resultados




def guardar_estado_cuenta(banco,p_fecha_inicio ,p_fecha_fin ,documento):
    if not banco: 
        mensajes.mensajes_Error("Debe ingresar un banco")
        return 
    if not p_fecha_inicio: 
        mensajes.mensajes_Error("Debe ingresar fecha inicio")
        return
    if not p_fecha_fin: 
        mensajes.mensajes_Error("Debe ingresar fecha fin")
        return
    if not documento: 
        mensajes.mensajes_Error("Debe adjuntar un documento")
        return



    # Obtener dinámicamente el ID 
    banco_id = controlador_banco.obtener_banco_id(banco)

    # Validar si el ID fue encontrado correctamente 
    if banco_id is None:
        mensajes.mensajes_Error("Cuenta no encontrada en la base de datos")
        return
    
    if isinstance(banco_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Cuenta: {banco}")
        return   

    accion = estado_cuenta.insertar_estado_cuenta(banco_id,p_fecha_inicio ,p_fecha_fin ,documento)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_estado_cuenta(estado_cuenta_id): 
    if not estado_cuenta_id: 
        mensajes.mensajes_Error("Debe seleccionar un estado de cuenta ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el estado_cuenta con id: {estado_cuenta_id}?")

    if not respuesta:
        return

    accion = estado_cuenta.eliminar_estado_cuenta(estado_cuenta_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar el estado de cuenta con id {estado_cuenta_id}")

def actualizar_estado_cuenta(estado_cuenta_id,banco,p_fecha_inicio ,p_fecha_fin ,documento):
    if not estado_cuenta_id: 
        mensajes.mensajes_Error("Debe seleccionar un estado de cuenta")
        return  
    if not banco: 
        mensajes.mensajes_Error("Debe ingresar un banco")
        return 
    if not p_fecha_inicio: 
        mensajes.mensajes_Error("Debe ingresar fecha inicio")
        return
    if not p_fecha_fin: 
        mensajes.mensajes_Error("Debe ingresar fecha fin")
        return


    # Obtener dinámicamente el ID 
    banco_id = controlador_banco.obtener_banco_id(banco)

    # Validar si el ID fue encontrado correctamente 
    if banco_id is None:
        mensajes.mensajes_Error("Cuenta no encontrada en la base de datos")
        return
    
    if isinstance(banco_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Cuenta: {banco}")
        return   

    accion = estado_cuenta.actualizar_estado_cuenta(estado_cuenta_id,banco_id,p_fecha_inicio ,p_fecha_fin ,documento)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito")


def filtrar_estado_cuenta(fecha_inicio, fecha_fin):
    # Validar que ambos tengan valor
    if not fecha_inicio or not fecha_fin:
        mensajes.mensajes_Error("Debe ingresar ambas fechas: inicio y fin.")
        return []


    resultados = estado_cuenta.filtrar_fecha(fecha_inicio, fecha_fin)
    
    if isinstance(resultados, str):  # error como string
        mensajes.mensajes_Error(f"Error: {resultados}")
        return
    
    if resultados:
        return resultados