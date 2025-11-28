#!/usr/bin/env python3
"""
Script para probar la conexión directa a la base de datos y verificar los datos.
"""
import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import db
from app.domain.models import ObraSocial
from sqlmodel import select

def test_database_connection():
    print("🔍 Probando conexión a la base de datos...")
    
    try:
        # Obtener la sesión
        session = db.get_session
        print("✅ Conexión exitosa")
        
        # Contar todas las obras sociales
        count_statement = select(ObraSocial)
        result = session.exec(count_statement)
        obras_sociales = list(result.all())
        
        print(f"📊 Total de obras sociales encontradas: {len(obras_sociales)}")
        
        if obras_sociales:
            print("\n📋 Obras sociales en la base de datos:")
            for i, obra in enumerate(obras_sociales, 1):
                print(f"{i}. {obra.nombre} - CUIT: {obra.cuit} - Cobertura: {obra.porcentaje_cobertura}%")
        else:
            print("⚠️  No se encontraron obras sociales en la base de datos")
            
            # Verificar si hay tablas
            print("🔍 Verificando estructura de la base de datos...")
            from sqlmodel import text
            tables_result = session.exec(text("SHOW TABLES"))
            tables = list(tables_result.all())
            print(f"📊 Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
        
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection()