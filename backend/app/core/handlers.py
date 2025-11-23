# app/core/handlers.py
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.core.exceptions import RecursoNoEncontradoException, ReglaDeNegocioException

class ManejadorDeExcepciones:
    """
    Centraliza cómo se transforman las excepciones en respuestas HTTP JSON.
    """

    @staticmethod
    async def not_found_handler(request: Request, exc: RecursoNoEncontradoException):
        return JSONResponse(
            status_code=404,
            content={
                "error": "Recurso no encontrado",
                "mensaje": exc.mensaje,
                "path": request.url.path
            }
        )

    @staticmethod
    async def business_rule_handler(request: Request, exc: ReglaDeNegocioException):
        return JSONResponse(
            status_code=400, # Bad Request
            content={
                "error": "Error de Regla de Negocio",
                "mensaje": exc.mensaje
            }
        )

    @staticmethod
    async def general_handler(request: Request, exc: Exception):
        # Captura cualquier error no controlado (NullPointer, etc.)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error Interno del Servidor",
                "mensaje": "Ocurrió un error inesperado. Contacte a soporte."
            }
        )

    # Método estático para registrar todo en la APP
    @staticmethod
    def configurar_handlers(app: FastAPI):
        app.add_exception_handler(RecursoNoEncontradoException, ManejadorDeExcepciones.not_found_handler)
        app.add_exception_handler(ReglaDeNegocioException, ManejadorDeExcepciones.business_rule_handler)
        app.add_exception_handler(Exception, ManejadorDeExcepciones.general_handler)