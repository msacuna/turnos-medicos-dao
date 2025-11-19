from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import validate_db_schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- CÓDIGO DE ARRANQUE ---
    print("🚀 Iniciando Turnero Médico...")
    try:
        validate_db_schema() # Valida que las tablas existan
    except Exception as e:
        print("⚠️ La aplicación inició con errores de base de datos.")
        # Si quieres que la app NO arranque si la BD está mal, descomenta la línea de abajo:
        raise e 
    
    yield # Aquí corre la aplicación
    
    # --- CÓDIGO DE CIERRE ---
    print("🛑 Apagando Turnero Médico...")


app = FastAPI(
    title="Turnero Médico API",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"status": "ok", "mensaje": "API funcionando correctamente 🏥"}