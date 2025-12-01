from models.model_party import Party
from controllers import controlador_naturaleza_party,controlador_cliente
from utils.mensajes import mensajes


party = Party()

def mostrar_personas():
    resultados = party.obtener_personas()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def buscar_party(nombre):
    if not nombre:
        mensajes.mensajes_Error("Debe ingresar un nombre")  
        return

    resultados = party.buscar_persona(nombre)

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return  mensajes.mensajes_informacion("No se encontro a la persona")

    return resultados

def guardar_persona(nombre, descripcion_naturaleza):
    if not nombre: 
        mensajes.mensajes_Error("Debe ingresar un nombre")
        return None
    if not descripcion_naturaleza: 
        mensajes.mensajes_Error("Debe Seleccionar una Naturaleza")
        return None

    # Obtener dinámicamente el ID de la naturaleza
    id_naturaleza = controlador_naturaleza_party.obtener_naturaleza_id_1(descripcion_naturaleza)

    # Validar si el ID fue encontrado correctamente
    if id_naturaleza is None:
        mensajes.mensajes_Error("Naturaleza no encontrada en la base de datos")
        return None
    if isinstance(id_naturaleza, str):
        mensajes.mensajes_Error(f"Error al obtener naturaleza: {id_naturaleza}")
        return None

    party_id = party.insertar_persona(nombre, id_naturaleza)

    if isinstance(party_id, str):  # error como string
        mensajes.mensajes_Error(f"Error: {party_id}")
        return None

    mensajes.mensajes_informacion("Éxito en la inserción")
    return party_id


def eliminar_persona(persona_id): 
    if not persona_id: 
        mensajes.mensajes_Error("Debe seleccionar una persona")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar a persona con id: {persona_id}?")

    if not respuesta:
        return

    accion = party.eliminar_persona(persona_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    if accion: 
        controlador_cliente.eliminar_cliente(persona_id)
        mensajes.mensajes_informacion(f"Éxito en eliminar a persona con id {persona_id}")

def actualizar_party(persona_id,nombre, descripcion_naturaleza): 
    if not persona_id:
        mensajes.mensajes_Error("Debe seleccionar una persona de la tabla")
        return
    if not nombre: 
        mensajes.mensajes_Error("Debe ingresar un nombre")
        return 
    if not descripcion_naturaleza: 
        mensajes.mensajes_Error("Debe Seleccionar una Naturaleza")
        return

    # Obtener dinámicamente el ID de la naturaleza
    id_naturaleza = controlador_naturaleza_party.obtener_naturaleza_id_1(descripcion_naturaleza)
    
    # Validar si el ID fue encontrado correctamente
    if id_naturaleza is None:
        mensajes.mensajes_Error("Naturaleza no encontrada en la base de datos")
        return
    if isinstance(id_naturaleza, str):
        mensajes.mensajes_Error(f"Error al obtener naturaleza: {id_naturaleza}")
        return

    accion = party.actualizar_persona(persona_id,nombre,id_naturaleza)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en actualizar a  {nombre}")


def filtrar_por_naturaleza(naturaleza):
        if not naturaleza: 
            mensajes.mensajes_Error("Debe seleccionar una naturaleza para aplicar el filtro")

        resultado = party.filtro_naturaleza(naturaleza)
        
        if isinstance(resultado, str):  # error como string
            mensajes.mensajes_Error(f"Error: {resultado}")
            return
        return resultado

def obtener_party_id(nombre):
    return party.obtener_party_id(nombre)