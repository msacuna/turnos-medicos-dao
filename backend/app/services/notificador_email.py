from backend.app.services.interfaces.observador_turno import ObservadorTurno


class NotificadorEmail(ObservadorTurno):
    def __init__(self):
        # Cambiar el template a:
        self.mensaje = "Lamentamos informarle que su turno del {} ha sido cancelado"

    def actualizar(self, pacientes: list[list[str]]):
        for paciente in pacientes:
            email = paciente[0]
            fecha_hora = paciente[2]
            # Insertar la fecha_hora en el mensaje
            # Usar:
            mensaje_personalizado = self.mensaje.format(fecha_hora)
            # Lógica para enviar el email
            print(f"Enviando email a {email}: {mensaje_personalizado}")