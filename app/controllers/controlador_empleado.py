# controllers/controller_empleado.py
from models.model_empleado import Empleado
from controllers import controlador_party
from utils.mensajes import mensajes

empleado = Empleado()

# ──────────────────────────── CREAR ────────────────────────────
def guardar_empleado(primer_apellido, segundo_apellido, fecha_nacimiento, party) -> None:
    if not primer_apellido or not segundo_apellido:
        mensajes.mensajes_Error("Debe ingresar ambos apellidos")
        return
    if not fecha_nacimiento:
        mensajes.mensajes_Error("Debe ingresar una fecha de nacimiento")
        return
    if not party:
        mensajes.mensajes_Error("Debe seleccionar una entidad asociada (party)")
        return
    
    # Obtener dinámicamente el ID
    party_id = controlador_party.obtener_party_id(party)

    # Validar si el ID fue encontrado correctamente
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la persona: {party_id}")
        return   
    

    accion = empleado.insertar_empleado(primer_apellido, segundo_apellido, fecha_nacimiento, party_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Empleado registrado exitosamente")


# ──────────────────────────── ELIMINAR ─────────────────────────
def eliminar_empleado(empleado_id: int) -> None:
    if not empleado_id:
        mensajes.mensajes_Error("Debe seleccionar un empleado para eliminar")
        return

    respuesta = mensajes.mensajes_askyesno(
        f"¿Desea eliminar el empleado con ID: {empleado_id}?"
    )
    if not respuesta:
        return

    accion = empleado.eliminar_empleado(empleado_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion(
            f"Empleado con ID {empleado_id} eliminado exitosamente"
        )


# ──────────────────────────── LISTAR ───────────────────────────
def mostrar_empleados():
    resultados = empleado.obtener_empleados()

    if isinstance(resultados, str):
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:
        return None

    return resultados


# ──────────────────────────── ACTUALIZAR ───────────────────────
def actualizar_empleado(empleado_id: int, primer_apellido: str, segundo_apellido: str, fecha_nacimiento: str, party) -> None:
    if not empleado_id:
        mensajes.mensajes_Error("Debe seleccionar un empleado para actualizar")
        return
    if not primer_apellido or not segundo_apellido:
        mensajes.mensajes_Error("Debe ingresar ambos apellidos")
        return
    if not fecha_nacimiento:
        mensajes.mensajes_Error("Debe ingresar una fecha de nacimiento")
        return
    if not party:
        mensajes.mensajes_Error("Debe seleccionar una entidad asociada (party)")
        return

    # Obtener dinámicamente el ID
    party_id = controlador_party.obtener_party_id(party)

    # Validar si el ID fue encontrado correctamente
    if party_id is None:
        mensajes.mensajes_Error("Persona no encontrada en la base de datos")
        return
    
    if isinstance(party_id, str):
        mensajes.mensajes_Error(f"Error al obtener la persona: {party_id}")
        return   
    
    accion = empleado.actualizar_empleado(empleado_id, primer_apellido, segundo_apellido, fecha_nacimiento, party_id)

    if isinstance(accion, str):
        mensajes.mensajes_Error(f"Error: {accion}")
        return

    if accion:
        mensajes.mensajes_informacion("Empleado actualizado exitosamente")


# ──────────────────────────── OBTENER ID ───────────────────────
def obtener_empleado_id(nombre_completo: str):
    """
    Devuelve el ID del empleado a partir del nombre completo.
    """
    return empleado.obtener_empleado_id(nombre_completo)


def mostrar_nombre_completo():
    resultados = empleado.obtener_nombre_completo()

    if isinstance(resultados, str):
        mensajes.mensajes_Error(f"Error: {resultados}")
        return None

    if not resultados:
        return None

    return resultados


def buscar_empleado(primer_apellido, segundo_apellido): 
    if not primer_apellido or not segundo_apellido:
        mensajes.mensajes_Error("Debe ingresar ambos apellidos")
        return
        
    resultados = empleado.buscar_empleado_por_apellidos(primer_apellido,segundo_apellido)

    if isinstance(resultados, str):  # error como string
        mensajes.mensajes_Error( f"Error: {resultados}")
        return
    
    if not resultados:  # lista vacía
         mensajes.mensajes_informacion("No se encontro al empleado")
         return

    return resultados


def buscar_por_nombre_completo(nombre_completo): 
    if not nombre_completo:
        mensajes.mensajes_Error("Debe Seleccionar un filtro")
        
    resultados = empleado.buscar_empleado_por_nombre_completo(nombre_completo)

    if isinstance(resultados, str):  # error como string
        return f"Error: {resultados}"
    
    if not resultados:  # lista vacía
        return  mensajes.mensajes_informacion("No se encontro al empleado")

    return resultados
