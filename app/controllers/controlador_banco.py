from models.model_banco import Banco
from controllers import  controlador_party

from utils.mensajes import mensajes


banco  = Banco()

def mostrar_banco():
    resultados = banco.obtener_banco()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    

    return resultados

def traer_cuenta_iban(): 
    resultados = banco.obtener_cuenta_iban()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    
    return resultados


def guardar_banco(nombre_banco,cuenta_iban,cuenta_cliente,party):
    if not nombre_banco: 
        mensajes.mensajes_Error("Debe ingresar un nombre")
        return 
    if not cuenta_iban: 
        mensajes.mensajes_Error("Debe ingresar la cuenta iban")
        return
    if not party: 
        mensajes.mensajes_Error("Debe Seleccionar una persona")
        return


    # Obtener dinámicamente el ID de la naturaleza
    party_id = controlador_party.obtener_party_id(party)

    # Validar si el ID fue encontrado correctamente 
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Persona: {party_id}")
        return   

    accion = banco.insertar_banco(nombre_banco,cuenta_iban,cuenta_cliente,party_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_banco(banco_id): 
    if not banco_id: 
        mensajes.mensajes_Error("Debe seleccionar un banco ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el banco con id: {banco_id}?")

    if not respuesta:
        return

    accion = banco.eliminar_banco(banco_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar el banco con id {banco_id}")

def actualizar_banco(banco_id,nombre_banco,cuenta_iban,cuenta_cliente,party):
    if not banco_id: 
        mensajes.mensajes_Error("Debe ingresar seleccionar un banco")
        return 
    if not nombre_banco: 
        mensajes.mensajes_Error("Debe ingresar un nombre")
        return 
    if not cuenta_iban: 
        mensajes.mensajes_Error("Debe ingresar la cuenta iban")
        return
    if not party: 
        mensajes.mensajes_Error("Debe Seleccionar una persona")
        return


    # Obtener dinámicamente el ID de la naturaleza
    party_id = controlador_party.obtener_party_id(party)

    # Validar si el ID fue encontrado correctamente 
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Persona: {party_id}")
        return   

    accion = banco.actualizar_banco(banco_id,nombre_banco,cuenta_iban,cuenta_cliente,party_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito")

def filtrar_banco(nombre_banco, nombre_party):
    filtro_banco = nombre_banco
    filtro_party = nombre_party

    # Validar que al menos uno tenga valor
    if not filtro_banco and not filtro_party:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro.")
        return []

    # Asegurar que se envíen strings al método del modelo
    nombre_banco = nombre_banco or ''
    nombre_party = nombre_party or ''

    try:
        resultado = banco.filtrar_bancos(nombre_banco, nombre_party)
        return resultado

    except Exception as e:
        mensajes.mensajes_Error(f"Ocurrió un error al filtrar: {e}")
        return []


def obtener_banco_id(cuenta):
    return banco.obtener_banco_id(cuenta)