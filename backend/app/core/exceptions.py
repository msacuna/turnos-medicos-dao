# app/core/exceptions.py

class BaseAppException(Exception):
    """Excepción base para tu aplicación"""
    def __init__(self, mensaje: str):
        self.mensaje = mensaje

class RecursoNoEncontradoException(BaseAppException):
    """Equivalente a EntityNotFoundException en Java"""
    pass

class ReglaDeNegocioException(BaseAppException):
    """Para validaciones lógicas (ej: Alergia duplicada)"""
    pass

