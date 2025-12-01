from models.model_identificacion import Identificacion
from controllers import controlador_nacionalidad,controlador_party,controlador_tipo_identificaciones
from utils.mensajes import mensajes


identificacion = Identificacion()

def mostrar_identificaciones():
    resultados = identificacion.obtener_identificaciones()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    

    return resultados

def buscar_identificacion(nombre):
    if not nombre:
        mensajes.mensajes_Error("Debe seleccionar una persona")  
        return

    resultados = identificacion.buscar_identificacion(nombre)

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return  mensajes.mensajes_informacion("No se encontro la identificacion")

    return resultados


def guardar_identificacion(valor,tipo_identificacion,nacionalidad,party):
    if not valor: 
        mensajes.mensajes_Error("Debe ingresar un valor")
        return 
    if not tipo_identificacion: 
        mensajes.mensajes_Error("Debe Seleccionar un tipo identificacion")
        return
    if not nacionalidad: 
        mensajes.mensajes_Error("Debe Seleccionar una nacionalidad")
        return
    if not party: 
        mensajes.mensajes_Error("Debe Seleccionar una persona")
        return


    # Obtener dinámicamente el ID de la naturaleza
    tipo_identificacion_id = controlador_tipo_identificaciones.obtener_tipo_identificacion_id(tipo_identificacion)
    nacionalidad_id = controlador_nacionalidad.obtener_nacionalidad_id(nacionalidad)
    party_id = controlador_party.obtener_party_id(party)

    # Validar si el ID fue encontrado correctamente
    if tipo_identificacion_id is None:
        mensajes.mensajes_Error("Tipo identificacion no encontrada en la base de datos")
        return
    if isinstance(tipo_identificacion_id, str):
        mensajes.mensajes_Error(f"Error al obtener Tipo Identificacion: {tipo_identificacion_id}")
        return
    if nacionalidad_id is None:
        mensajes.mensajes_Error("Nacionaldad no encontrada en la base de datos")
        return
    if isinstance(nacionalidad_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Nacionaldad: {nacionalidad_id}")
        return   
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Persona: {party_id}")
        return   

    accion = identificacion.insertar_identificacion(valor,tipo_identificacion_id,nacionalidad_id,party_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_identificacion(identificacion_id): 
    if not identificacion_id: 
        mensajes.mensajes_Error("Debe seleccionar una identificacion")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar la identificacion con id: {identificacion_id}?")

    if not respuesta:
        return

    accion = identificacion.eliminar_identificacion(identificacion_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar la identificacion con id {identificacion_id}")


def actualizar_party(identificacion_id,valor,tipo_identificacion, nacionalidad,party): 
    if not valor: 
        mensajes.mensajes_Error("Debe ingresar un valor")
        return 
    if not tipo_identificacion: 
        mensajes.mensajes_Error("Debe Seleccionar un tipo identificacion")
        return
    if not nacionalidad: 
        mensajes.mensajes_Error("Debe Seleccionar una nacionalidad")
        return
    if not party: 
        mensajes.mensajes_Error("Debe Seleccionar una persona")
        return
        
    # Obtener dinámicamente el ID de la naturaleza
    tipo_identificacion_id = controlador_tipo_identificaciones.obtener_tipo_identificacion_id(tipo_identificacion)
    nacionalidad_id = controlador_nacionalidad.obtener_nacionalidad_id(nacionalidad)
    party_id = controlador_party.obtener_party_id(party)

     # Validar si el ID fue encontrado correctamente
    if tipo_identificacion_id is None:
        mensajes.mensajes_Error("Tipo identificacion no encontrada en la base de datos")
        return
    if isinstance(tipo_identificacion_id, str):
        mensajes.mensajes_Error(f"Error al obtener Tipo Identificacion: {tipo_identificacion_id}")
        return
    if nacionalidad_id is None:
        mensajes.mensajes_Error("Nacionaldad no encontrada en la base de datos")
        return
    if isinstance(nacionalidad_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Nacionaldad: {nacionalidad_id}")
        return   
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Persona: {party_id}")
        return   

    accion = identificacion.actualizar_identificacion(identificacion_id, valor,tipo_identificacion_id,nacionalidad_id,party_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en actualizar a  {party}")


def filtrar_identificaciones(tipo, nombre):
    if not tipo and not nombre:
        mensajes.mensajes_Error("Debe seleccionar al menos un filtro")
        return []

    try:
        if tipo and nombre:
            resultado = identificacion.filtrar_por_tipo_y_nombre(tipo, nombre)
        elif tipo:
            resultado = identificacion.filtrar_por_tipo(tipo)
        elif nombre:
            resultado = identificacion.buscar_identificacion(nombre)

        return resultado

    except Exception as e:
        mensajes.mensajes_Error(f"Ocurrió un error al filtrar: {str(e)}")
        return []

