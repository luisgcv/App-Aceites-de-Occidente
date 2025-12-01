# controllers/controller_empleado.py
from models.model_planilla import Planilla
from controllers import controlador_empleado
from utils.mensajes import mensajes


planilla =  Planilla()

# ──────────────────────────── CREAR ────────────────────────────
def guardar_planilla(empleado, fecha_inicio, fecha_fin, horas_trabajadas,pago_por_horas,salario,comentarios) -> None:
    if not empleado :
        mensajes.mensajes_Error("Debe ingresar un empleado")
        return
    if not fecha_inicio:
        mensajes.mensajes_Error("Debe ingresar una fecha de inicio")
        return
    if not fecha_fin:
        mensajes.mensajes_Error("Debe ingresar una fecha de fin")
        return
    if not comentarios:
        mensajes.mensajes_Error("Debe ingresar un comentario")
        return
    
    if salario:
        # caso válido: salario fijo
        pass
    elif horas_trabajadas and pago_por_horas:
        # caso válido: se calculará el salario
        salario = float(horas_trabajadas) * float(pago_por_horas)
    else:
        mensajes.mensajes_Error("Debe ingresar un salario fijo o ambos valores: horas trabajadas y pago por hora.")
        return

    # Obtener dinámicamente el ID
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)

    # Validar si el ID fue encontrado correctamente
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrada en la base de datos")
        return
    
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener al empleado: {empleado_id}")
        return   
    

    accion = planilla.insertar_planilla(empleado_id, fecha_inicio, fecha_fin, horas_trabajadas,pago_por_horas,salario,comentarios)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Planilla registrado exitosamente")


# ──────────────────────────── ELIMINAR ─────────────────────────
def eliminar_planilla(planilla_id: int) -> None:
    if not planilla_id:
        mensajes.mensajes_Error("Debe seleccionar una opcion para eliminar")
        return

    respuesta = mensajes.mensajes_askyesno(
        f"¿Desea eliminar el empleado con ID: {planilla_id}?"
    )
    if not respuesta:
        return

    accion = planilla.eliminar_planilla(planilla_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(
            f"Planilla con ID {planilla_id} eliminado exitosamente"
        )


# ──────────────────────────── LISTAR ───────────────────────────
def mostrar_planilla():
    resultados = planilla.obtener_planilla()

    if isinstance(resultados, str):
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:
        return None

    return resultados


# ──────────────────────────── ACTUALIZAR ───────────────────────
def actualizar_planilla(planilla_id,empleado, fecha_inicio, fecha_fin, horas_trabajadas,pago_por_horas,salario,comentarios) -> None:
    if not empleado :
        mensajes.mensajes_Error("Debe ingresar un empleado")
        return
    if not fecha_inicio:
        mensajes.mensajes_Error("Debe ingresar una fecha de inicio")
        return
    if not fecha_fin:
        mensajes.mensajes_Error("Debe ingresar una fecha de fin")
        return
    if not comentarios:
        mensajes.mensajes_Error("Debe ingresar un comentario")
        return
    if not planilla_id:
        mensajes.mensajes_Error("Debe seleccionar una planilla")
        return
    
    if salario:
        # caso válido: salario fijo
        pass
    elif horas_trabajadas and pago_por_horas:
        # caso válido: se calculará el salario
        salario = float(horas_trabajadas) * float(pago_por_horas)
    else:
        mensajes.mensajes_Error("Debe ingresar un salario fijo o ambos valores: horas trabajadas y pago por hora.")
        return

    # Obtener dinámicamente el ID
    empleado_id = controlador_empleado.obtener_empleado_id(empleado)

    # Validar si el ID fue encontrado correctamente
    if empleado_id is None:
        mensajes.mensajes_Error("Empleado no encontrada en la base de datos")
        return
    
    if isinstance(empleado_id, str):
        mensajes.mensajes_Error(f"Error al obtener al empleado: {empleado_id}")
        return   
    

    accion = planilla.actualizar_planilla(planilla_id,empleado_id, fecha_inicio, fecha_fin, horas_trabajadas,pago_por_horas,salario,comentarios)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Planilla actualizada exitosamente")








def filtrar_planilla(fecha_inicio, fecha_fin): 
    if not fecha_inicio:
        mensajes.mensajes_Error("Debe ingresar una fecha de inicio")
        return
    if not fecha_fin:
        mensajes.mensajes_Error("Debe ingresar una fecha de fin")
        return
    
    resultados = planilla.filtrar_planilla_fecha(fecha_inicio,fecha_fin)

    if isinstance(resultados, str):  # error como string
        mensajes.mensajes_informacion(f"Error: {resultados}")
        return 
    return resultados
