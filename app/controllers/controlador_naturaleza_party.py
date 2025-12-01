from models.model_naturaleza_party import Naturaleza_Party
from utils.mensajes import mensajes


naturaleza_party = Naturaleza_Party()


def guardar_naturaleza(descripcion): 
    if not descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return 
    
    accion = naturaleza_party.inrgesar_naturaleza(descripcion)
    if isinstance(accion, str):  # error como string
            mensajes.mensajes_Error(f"Error: {accion}")
            return
    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")

def eliminar_naturaleza(id_naturaleza):

    if not id_naturaleza: 
        mensajes.mensajes_Error("Debe seleccionar una naturaleza")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar la naturaleza con id: {id_naturaleza}?")

    if not respuesta:
        return

    accion = naturaleza_party.eliminar_naturaleza(id_naturaleza)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar la naturaleza con id {id_naturaleza}")




def mostrar_naturaleza():
    resultados = naturaleza_party.obtener_naturaleza()

    if isinstance(resultados, str):  # error como string
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:  # lista vacía
        return None

    return resultados



def actualizar_naturaleza(naturaleza_id, descripcion): 
    if not naturaleza_id:
        mensajes.mensajes_Error("Debe seleccionar una naturaleza de la tabla")
        return
    if not descripcion: 
        mensajes.mensajes_Error("Debe ingresar un descripcion")
        return 

    accion = naturaleza_party.actualizar_naturaleza(naturaleza_id,descripcion)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en actualizar a  {descripcion}")
    return 


def cargar_naturaleza(naturaleza_id): 
    if not id: 
        mensajes.mensajes_Error("Debe seleccionar una naturaleza")


    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar a naturaleza con id: {naturaleza_id}?")

    if not respuesta:
        return

    accion = naturaleza_party.eliminar_naturaleza(naturaleza_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar la naturaleza con id {naturaleza_id}")

def obtener_naturaleza_id_1(descripcion_naturaleza):
    return naturaleza_party.obtener_naturaleza_id(descripcion_naturaleza)