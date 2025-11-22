import time
from sqlmodel import SQLModel, create_engine, Session, inspect
from sqlalchemy.exc import OperationalError
from contextvars import ContextVar
from typing import Optional
from .config import settings

# 1. Configuración del Engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 2. Función para obtener sesión de DB
_current_session: ContextVar[Optional[Session]] = ContextVar("current_session", default=None)

class DatabaseManagerSingleton:
    _instance: Optional["DatabaseManagerSingleton"] = None

    def __new__(cls) -> "DatabaseManagerSingleton":
        if cls._instance is None:
            cls._instance = super(DatabaseManagerSingleton, cls).__new__(cls)
        return cls._instance

    @property
    def get_session(self) -> Session:
        current_session = _current_session.get()
        if current_session is None:
            current_session = Session(engine)
            _current_session.set(current_session)
        return current_session
    
db = DatabaseManagerSingleton()

def get_session():
    with db.get_session as session:
        yield session

# Faltaria cerrar la session en algun momento?

def validate_db_schema():
    """
    Compara las tablas de la Base de Datos contra los Modelos de SQLModel.
    Lanza error si falta alguna tabla.
    """
    # ¡VITAL! Importar 'models' aquí fuerza a que SQLModel lea todos tus archivos
    # y registre las clases en 'metadata'. Sin esto, model_tables estaría vacío.
    from app.domain import models

    print("🔍 Iniciando validación de esquema...")

    max_retries = 10  # Intentará durante ~20 segundos (10 * 2s)
    wait_seconds = 2

    for attempt in range(max_retries):
        try:
            # Intentamos conectar. Si falla aquí, salta al except.
            inspector = inspect(engine)
            
            # --- Si llega aquí, la conexión fue exitosa ---
            
            db_tables = set(inspector.get_table_names())
            model_tables = set(SQLModel.metadata.tables.keys())
            missing_tables = model_tables - db_tables

            if missing_tables:
                error_msg = f"❌ ERROR CRÍTICO: Faltan tablas en la base de datos: {missing_tables}"
                print(error_msg)
                raise RuntimeError(error_msg)
            
            print(f"✅ Validación exitosa: Se encontraron {len(model_tables)} tablas sincronizadas.")
            return # Salimos de la función con éxito
            
        except OperationalError as e:
            # Capturamos errores de conexión (como el 2013 Lost Connection)
            if attempt < max_retries - 1:
                print(f"⏳ La base de datos aún no está lista (Intento {attempt + 1}/{max_retries}). Reintentando en {wait_seconds}s...")
                time.sleep(wait_seconds)
            else:
                print(f"🚨 Falló la conexión después de {max_retries} intentos.")
                raise e # Si fallan todos, lanzamos el error real
                
        except Exception as e:
            # Cualquier otro error (ej: tablas faltantes) rompe inmediatamente
            print(f"🚨 Error inesperado en validación: {e}")
            raise e