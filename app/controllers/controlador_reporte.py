from models.model_reportes import Reportes

from utils.mensajes import mensajes


reporte  = Reportes()


def mostrar_total_ingresos_mes():
    resultados = reporte.obtener_total_ingresos_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_total_gasto_mes():
    resultados = reporte.obtener_total_gasto_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_total_factura_mes():
    resultados = reporte.obtener_total_factura_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_total_factura_estado_mes():
    resultados = reporte.obtener_total_factura_estado_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_total_retiros_mes():
    resultados = reporte.obtener_total_retiros_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_total_transacciones_mes():
    resultados = reporte.obtener_total_transacciones_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_total_balance_mes():
    resultados = reporte.obtener_total_balance_mes()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 

    return resultados


def mostrar_ganancia_neta(fecha_inicio, fecha_fin):

    # Validar que al menos uno tenga valor
    if not fecha_fin and not fecha_inicio:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro.")
        return []
    
    resultado = reporte.obtener_ganancia_neta(fecha_inicio, fecha_fin)

    if isinstance(resultado, str):  # error como string
        mensajes.mensajes_Error(f"Error: {resultado}")
        return

    return resultado

def mostrar_salario_empleado(empleado, fecha_inicio, fecha_fin):

    # Validar que al menos uno tenga valor
    if not fecha_fin and not fecha_inicio and not empleado:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro.")
        return []
    
    resultado = reporte.obtener_salario_empleado(empleado,fecha_inicio, fecha_fin)

    if isinstance(resultado, str):  # error como string
        mensajes.mensajes_Error(f"Error: {resultado}")
        return

    return resultado






 