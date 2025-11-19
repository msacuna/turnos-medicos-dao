from sqlmodel import SQLModel, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from app.core.config import settings

# 1. Configuración del Engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, # Verifica conexión antes de usarla
    pool_recycle=300    # Recicla conexiones cada 5 min
)
# 2. Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Dependencia para FastAPI (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. VALIDACIÓN DE ESQUEMA (Simple y Directa)
def validate_db_schema():
    """
    Compara las tablas de la Base de Datos contra los Modelos de SQLModel.
    Lanza error si falta alguna tabla.
    """
    # ¡VITAL! Importar 'models' aquí fuerza a que SQLModel lea todos tus archivos
    # y registre las clases en 'metadata'. Sin esto, model_tables estaría vacío.
    from app import models 

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