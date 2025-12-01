from models.model_cliente import Cliente
from utils.mensajes import mensajes

cliente = Cliente()

def hacer_cliente(party_id):
    if not party_id: 
        mensajes.mensajes_Error("Debe ingresar si es cliente o no")
        return 

    # Verificar si ya es cliente
    es_cliente_ya = cliente.es_cliente(party_id)
    
    if isinstance(es_cliente_ya, str):  # Error al consultar
        mensajes.mensajes_Error(f"Error al verificar cliente: {es_cliente_ya}")
        return

    if es_cliente_ya:
        return

    # Insertar cliente sólo si no existe
    accion = cliente.insertar_cliente(party_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

def eliminar_cliente(party_id):
    return cliente.eliminar_cliente(party_id)

def mostrar_clientes():
    resultados = cliente.obtener_cliente()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados