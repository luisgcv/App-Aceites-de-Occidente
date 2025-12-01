from models.model_dashboard import Inicio

from utils.mensajes import mensajes


dashboard  = Inicio()

def mostrar_factura_pendiente():
    resultados = dashboard.obtener_factura_pendiente()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_total_gastos_mes():
    resultados = dashboard.obtener_total_gastos_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_ingresos_mensuales():
    resultados = dashboard.obtener_ingresos_mensuales()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_ultimos_gastos():
    resultados = dashboard.obtener_ultimos_gastos()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_transacciones_recientes():
    resultados = dashboard.obtener_transacciones_recientes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados



def mostrar_factura_estado():
    resultados = dashboard.obtener_factura_estado()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_retiros_recientes():
    resultados = dashboard.obtener_retiros_recientes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados



