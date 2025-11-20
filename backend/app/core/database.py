from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import inspect
from .config import settings

# 1. Configuración del Engine
engine = create_engine(settings.DATABASE_URL)

# 2. Función para obtener sesión de DB
def get_session():
    with Session(engine) as session:
        yield session

def validate_db_schema():
    """
    Compara las tablas de la Base de Datos contra los Modelos de SQLModel.
    Lanza error si falta alguna tabla.
    """
    # ¡VITAL! Importar 'models' aquí fuerza a que SQLModel lea todos tus archivos
    # y registre las clases en 'metadata'. Sin esto, model_tables estaría vacío.
    from app.domain import models

    print("🔍 Iniciando validación de esquema...")
    
    try:
        inspector = inspect(engine)
        
        # A. Tablas que existen REALMENTE en MySQL
        db_tables = set(inspector.get_table_names())
        
        # B. Tablas que tú definiste en PYTHON (SQLModel)
        model_tables = set(SQLModel.metadata.tables.keys())

        # C. Comparación
        missing_tables = model_tables - db_tables

        if missing_tables:
            error_msg = f"❌ ERROR CRÍTICO: Faltan tablas en la base de datos: {missing_tables}"
            print(error_msg)
            raise RuntimeError(error_msg)
        
        print(f"✅ Validación exitosa: Se encontraron {len(model_tables)} tablas sincronizadas.")
        
    except Exception as e:
        print(f"🚨 Falló la conexión o validación: {e}")
        raise e # Relanzamos para que main.py decida si detiene la app