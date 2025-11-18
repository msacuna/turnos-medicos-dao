from fastapi import FastAPI
from app.core.database import validate_db

app = FastAPI()


"""Una vez creadas las tablas, validamos y eliminamos esta función"""
@app.on_event("startup")
async def startup_event():
    try:
        validate_db()
    except Exception as e:
        print(f"Error al validar esquema de BD: {e}")


@app.get("/")
def root():
    return {"mensaje": "API funcionando 🚀"}