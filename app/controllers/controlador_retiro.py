from models.model_retiros import Retiro
from controllers import  controlador_banco,controlador_empleado

from utils.mensajes import mensajes


retiro  = Retiro()

def mostrar_retiro():
    resultados = retiro.obtener_retiro()

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return None 
    

    return resultados




def guardar_retiro(descripcion,monto ,fecha ,empleado,banco):
    if not descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return 
    if not monto: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar fecha ")
        return
    if not empleado: 
        mensajes.mensajes_Error("Debe seleccionar un empleado")
        return
    if not banco: 
        mensajes.mensajes_Error("Debe seleccionar un banco")
        return

    # Obtener dinámicamente el ID 
    banco_id = controlador_banco.obtener_banco_id(banco)
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)

    # Validar si el ID fue encontrado correctamente 
    if banco_id is None:
        mensajes.mensajes_Error("Cuenta no encontrada en la base de datos")
        return
    
    if isinstance(banco_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Cuenta: {banco}")
        return   
    
    # Validar si el ID fue encontrado correctamente 
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrado en la base de datos")
        return
    
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener el empleado: {empleado_id}")
        return   

    accion = retiro.insertar_retiro(descripcion,monto ,fecha ,empleado_id,banco_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito en la inserción")


def eliminar_retiro(retiro_id): 
    if not retiro_id: 
        mensajes.mensajes_Error("Debe seleccionar un retiro ")
        return 

    respuesta = mensajes.mensajes_askyesno(f"¿Eliminar el retiro con id: {retiro_id}?")

    if not respuesta:
        return

    accion = retiro.eliminar_retiro(retiro_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return
    
    if accion: 
        mensajes.mensajes_informacion(f"Éxito en eliminar el retiro con id {retiro_id}")


def actualizar_retiro(retiro_id,descripcion,monto ,fecha ,empleado,banco):
    if not retiro_id: 
        mensajes.mensajes_Error("Debe seleccionar un retiro")
        return 
    if not descripcion: 
        mensajes.mensajes_Error("Debe ingresar una descripcion")
        return 
    if not monto: 
        mensajes.mensajes_Error("Debe ingresar un monto")
        return
    if not fecha: 
        mensajes.mensajes_Error("Debe ingresar fecha ")
        return
    if not empleado: 
        mensajes.mensajes_Error("Debe seleccionar un empleado")
        return
    if not banco: 
        mensajes.mensajes_Error("Debe seleccionar un banco")
        return

    # Obtener dinámicamente el ID 
    banco_id = controlador_banco.obtener_banco_id(banco)
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)

    # Validar si el ID fue encontrado correctamente 
    if banco_id is None:
        mensajes.mensajes_Error("Cuenta no encontrada en la base de datos")
        return
    
    if isinstance(banco_id, str):
        mensajes.mensajes_Error(f"Error al obtener la Cuenta: {banco}")
        return   
    
    # Validar si el ID fue encontrado correctamente 
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrado en la base de datos")
        return
    
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener el empleado: {empleado_id}")
        return   

    accion = retiro.actualizar_retiro(retiro_id,descripcion,monto ,fecha ,empleado_id,banco_id)

    if isinstance(accion, str):  # error como string
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Éxito ")



def filtrar_retiro(fecha_inicio, fecha_fin,empleado):
        
    # Si no se selecciona ninguno, se lanza advertencia
    if not fecha_inicio and not fecha_fin and not empleado:
        mensajes.mensajes_Error("Debe seleccionar al menos un filtro.")
        return

    if not empleado: 
        empleado = None

    resultados = retiro.filtrar_retiro(fecha_inicio, fecha_fin,empleado)
    
    if isinstance(resultados, str):  # error como string
        mensajes.mensajes_Error(f"Error: {resultados}")
        return
    
    if resultados:
        return resultados
