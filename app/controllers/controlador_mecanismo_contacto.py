from models.modelo_mecanismo_contacto import MecanismoContacto
from controllers import controlador_tipo_mecanismo, controlador_party

from utils.mensajes import mensajes


mecanismo  = MecanismoContacto()

def mostrar_mecanismo():
    resultados = mecanismo.obtener_mecanismo_contacto()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    

    return resultados

def buscar_mecanismo(nombre):
    if not nombre:
        mensajes.mensajes_Error("Debe seleccionar un mecanismo")  
        return

    resultados = MecanismoContacto.buscar_medio_contacto(nombre)

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return  mensajes.mensajes_informacion("No se encontro el mecanismo")

    return resultados


def guardar_mecanismo(valor,prioridad,tipo,party):
    if not valor: 
        mensajes.mensajes_Error("Debe ingresar un valor")
        return 
    if not prioridad: 
        mensajes.mensajes_Error("Debe Seleccionar una prioridad")
        return
    if not tipo: 
        mensajes.mensajes_Error("Debe Seleccionar un tipo")
        return
    if not party: 
        mensajes.mensajes_Error("Debe Seleccionar una persona")
        return


    # Obtener dinámicamente el ID de la naturaleza
    tipo_mecanismo_id = controlador_tipo_mecanismo.obtener_tipo_mecanismo_id(tipo)
    party_id = controlador_party.obtener_party_id(party)

    # Validar si el ID fue encontrado correctamente

    if tipo_mecanismo_id is None:
        mensajes.mensajes_Error("Tipo de mecanismo no encontrada en la base de datos")
        return
    if isinstance(tipo_mecanismo_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Mecanismo : {tipo_mecanismo_id}")
        return   
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Persona: {party_id}")
        return   

    accion = mecanismo.insertar_medio_contacto(valor,prioridad,tipo_mecanismo_id,party_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_mecanismo(mecanismo_id): 
    if not mecanismo_id: 
        mensajes.mensajes_Error("Debe seleccionar un mecanismo de contacto ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el mecanismo de contacto con id: {mecanismo_id}?")

    if not respuesta:
        return

    accion = mecanismo.eliminar_medio_contacto(mecanismo_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar el mecanismo con id {mecanismo_id}")


def actualizar_mecanismo(medio_contacto_id,valor,prioridad, tipo,party): 
    if not valor: 
        mensajes.mensajes_Error("Debe ingresar un valor")
        return 
    if not medio_contacto_id: 
        mensajes.mensajes_Error("Debe Seleccionar un tipo")
        return
    if not prioridad: 
        mensajes.mensajes_Error("Debe Seleccionar una prioridad")
        return
    if not party: 
        mensajes.mensajes_Error("Debe Seleccionar una persona")
        return
        
    # Obtener dinámicamente el ID 
    tipo_mecanismo_id = controlador_tipo_mecanismo.obtener_tipo_mecanismo_id(tipo)
    party_id = controlador_party.obtener_party_id(party)


    # Validar si el ID fue encontrado correctamente
    if tipo_mecanismo_id is None:
        mensajes.mensajes_Error("Tipo de mecanismo no encontrada en la base de datos")
        return
    if isinstance(tipo_mecanismo_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Mecanismo : {tipo_mecanismo_id}")
        return   
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Persona: {party_id}")
        return   


    accion = mecanismo.actualizar_medio_contacto(medio_contacto_id,valor,prioridad,tipo_mecanismo_id,party_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en actualizar a  {party}")

def filtrar_mecanismo(tipo, nombre):
    tipo   = tipo or ''      # valor ESCALAR
    nombre = nombre or ''    # valor ESCALAR

    if not tipo and not nombre:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro.")
        return []

    try:
        resultado = mecanismo.filtrar_por_tipo_y_nombre(tipo, nombre)
        return resultado

    except Exception as e:
        mensajes.mensajes_Error(f"Ocurrió un error al filtrar: {e}")
        return []

