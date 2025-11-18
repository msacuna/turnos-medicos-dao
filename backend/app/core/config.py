from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "admin"
    DB_PASSWORD: str = "admin"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3307"
    DB_NAME: str = "turnos_medicos_bd"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()