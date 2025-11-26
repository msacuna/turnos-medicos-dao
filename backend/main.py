from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import validate_db_schema
from app.core.handlers import ManejadorDeExcepciones

from app.api.routes import *

# ESTO ES PARA VALIDAR LA BD AL INICIAR LA APP
# Podriamos eliminarlo en producción si queremos optimizar el arranque
# solamente muestra logs en la consola
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando Turnero Médico...")
    try:
        validate_db_schema() # Valida que las tablas existan
    except Exception as e:
        print("⚠️ La aplicación inició con errores de base de datos.")
        raise e 
    yield # Aquí corre la aplicación
    print("🛑 Apagando Turnero Médico...")

app = FastAPI(
    title="Turnero Médico API",
    lifespan=lifespan
)

ManejadorDeExcepciones.configurar_handlers(app)
app.include_router(pacientes_router)
app.include_router(profesionales_router)
app.include_router(alergias_router)
app.include_router(antecedentes_router)
app.include_router(especialidad_router)
app.include_router(medicamentos_router)
app.include_router(laboratorios_router)
app.include_router(obras_sociales_router)

@app.get("/")
def root():
    return {"status": "ok", "mensaje": "API funcionando correctamente 🏥"}