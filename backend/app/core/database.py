from sqlalchemy import create_engine, text # conexión a bd
from sqlalchemy.orm import sessionmaker, declarative_base # sesión para acceder a bd & base para modelos
from app.models import Base
from app.core.config import settings
import time

# Crear el motor SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear base para modelos
Base = declarative_base()

# PARA VER SI ESTAN TODAS LAS TABLAS
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300,    # Reciclar conexiones cada 5 minutos
    connect_args={
        "connect_timeout": 10,
        "read_timeout": 10,
        "write_timeout": 10
    }
)


# Validar esquema de bd (PARA VER SI ESTÁN TODAS LAS TABLAS)
def validate_db():
    """Valida que el esquema actual coincida con los modelos"""
    from sqlalchemy import inspect
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Verificar conexión básica primero
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Verificar que la base de datos existe y tiene tablas
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            if not existing_tables:
                raise Exception("❌ La base de datos está vacía. Ejecutar scripts de inicialización.")
            
            # Obtener tablas de los modelos
            model_tables = Base.metadata.tables.keys()
            
            # Verificar que todas las tablas existan
            missing_tables = []
            for table in model_tables:
                if table not in existing_tables:
                    missing_tables.append(table)
            
            if missing_tables:
                raise Exception(f"❌ Tablas faltantes: {', '.join(missing_tables)}")
            
            print(f"✅ Esquema validado correctamente - {len(existing_tables)} tablas encontradas")
            return
            
        except Exception as e:
            error_msg = str(e)
            
            # Errores de conexión que pueden resolverse con retry
            if any(x in error_msg for x in ["Lost connection", "Connection refused", "timeout", "Can't connect"]):
                if attempt < max_retries - 1:
                    print(f"🔄 Intento {attempt + 1}/{max_retries} falló, reintentando en {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"❌ Error de conexión después de {max_retries} intentos: MySQL no está disponible")
            
            # Otros errores específicos
            elif "Access denied" in error_msg:
                raise Exception(f"❌ Error de autenticación: Verificar usuario/contraseña")
            elif "Unknown database" in error_msg:
                raise Exception(f"❌ Base de datos '{settings.DB_NAME}' no existe")
            else:
                raise Exception(f"❌ Error de validación: {error_msg}")


# Obtener una sesión de bd
def get_db():
    db = SessionLocal()
    try:
        # Apertura y cierre de sesión automáticamente (evita fugas de conexiones)
        yield db
    finally:
        db.close()