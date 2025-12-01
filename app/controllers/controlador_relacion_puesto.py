from models.model_relacion_puesto import RelacionPuesto
from controllers import controlador_puesto,controlador_empleado

from utils.mensajes import mensajes


relacion  = RelacionPuesto()

def mostrar_relacion():
    resultados = relacion.obtener_relacion()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    

    return resultados

def buscar_relacion(nombre_completo):
    if not nombre_completo:
        mensajes.mensajes_Error("Debe seleccionar una opcion")  
        return

    resultados = relacion.buscar_relacion(nombre_completo)

    if isinstance(resultados, str):  # error como string
        return mensajes.mensajes_Error(f"Error: {resultados}")
    
    if not resultados:  # lista vacía
        return  mensajes.mensajes_informacion("No se encontro en la base de datos")

    return resultados


def guardar_relacion(empleado,p_puesto,p_descripcion):
    if not empleado: 
        mensajes.mensajes_Error("Debe ingresar escojer un empleado")
        return 
    if not p_puesto: 
        mensajes.mensajes_Error("Debe Seleccionar un puesto")
        return
    if not p_descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return



    # Obtener dinámicamente el ID
    p_puesto_id = controlador_puesto.obtener_puesto_id(p_puesto)
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)

    # Validar si el ID fue encontrado correctamente
    if p_puesto_id is None:
        mensajes.mensajes_Error("Puesto no encontrada en la base de datos")
        return
    if isinstance(p_puesto_id, str):
        mensajes.mensajes_Error(f"Error al obtener el puesto: {p_puesto_id}")
        return   
    # Validar si el ID fue encontrado correctamente
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrada en la base de datos")
        return
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener el Empleado: {empleado_id}")
        return   
    

    accion = relacion.insertar_relacion(empleado_id,p_puesto_id,p_descripcion)


    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_relacion(relacion_id): 
    if not relacion_id: 
        mensajes.mensajes_Error("Debe seleccionar una relacion ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar la relacion con id: {relacion_id}?")

    if not respuesta:
        return

    accion = relacion.eliminar_relacion(relacion_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar el mecanismo con id {relacion_id}")


def actualizar_mecanismo(relacion_id,empleado,p_puesto,p_descripcion): 
    if not relacion_id: 
        mensajes.mensajes_Error("Debe ingresar escojer una relacion")
        return 
    if not empleado: 
        mensajes.mensajes_Error("Debe ingresar escojer un empleado")
        return 
    if not p_puesto: 
        mensajes.mensajes_Error("Debe Seleccionar un puesto")
        return
    if not p_descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return



    # Obtener dinámicamente el ID
    p_puesto_id = controlador_puesto.obtener_puesto_id(p_puesto)
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)

    # Validar si el ID fue encontrado correctamente
    if p_puesto_id is None:
        mensajes.mensajes_Error("Puesto no encontrada en la base de datos")
        return
    if isinstance(p_puesto_id, str):
        mensajes.mensajes_Error(f"Error al obtener el puesto: {p_puesto_id}")
        return   
    # Validar si el ID fue encontrado correctamente
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrada en la base de datos")
        return
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener el Empleado: {empleado_id}")
        return   
    

    accion = relacion.actualizar_relacion(relacion_id,empleado_id,p_puesto_id,p_descripcion)


    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(f"Éxito en actualizar a {empleado}")


def filtrar_relacion(nombre_completo, puesto):
    nombre_completo = nombre_completo or ''
    puesto = puesto or ''

    if not nombre_completo and not puesto:
        mensajes.mensajes_Error("Debe ingresar al menos un filtro.")
        return []

    try:
        resultado = relacion.filtrar_por_nombre_puesto(nombre_completo, puesto)
        return resultado

    except Exception as e:
        mensajes.mensajes_Error(f"Ocurrió un error al filtrar: {e}")
        return []
