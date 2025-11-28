from .estado_turno_abs import Agendado, Cancelado, Ausente, Disponible, EnProceso, Finalizado

STATE_REGISTRY = {
    Agendado.nombre: Agendado,
    Cancelado.nombre: Cancelado,
    Ausente.nombre: Ausente,
    Disponible.nombre: Disponible,
    EnProceso.nombre: EnProceso,
    Finalizado.nombre: Finalizado
}

def build_estado_turno(nombre: str):
    estado_class = STATE_REGISTRY.get(nombre)
    if estado_class:
        return estado_class()
    else:
        raise ValueError(f"EstadoTurno '{nombre}' no reconocido.")