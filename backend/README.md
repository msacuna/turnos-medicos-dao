backend/
└── app/
    ├── api/
    │   ├── routes/
    ├── services/               # Lógica de negocio / casos de uso
    │   ├── user_service.py
    │   ├── report_service.py
    ├── crud/                   # Operaciones de BD puras (repositories)
    │   ├── user_crud.py
    │   ├── report_crud.py
    ├── schemas/                # Pydantic DTOs
    ├── core/                       # Configuración y seguridad
    │   ├── config.py                   # Configuración de JWT, DB, etc.
    │   ├── security.py                 # Funciones para JWT
    └── reports/                # Lógica de generación de informes/PDFs
    │   ├── report_generator.py     # Lógica para generar PDFs
    │   └── queries.py              # Consultas SQL específicas para reportes (opcional)
    ├── email_templates/
    ├── models/                 # Entidades SQLAlchemy
    │   ├── usuario.py
    │   ├── paciente.py
    │   ├── profesional.py
    │   ├── especialidad.py
    │   ├── obra_social.py
    │   ├── medicamento.py
    │   ├── laboratorio.py
    │   ├── turno.py
    │   ├── receta.py
    │   ├── diagnostico.py
    │   ├── antecedentes.py
    │   ├── alergia.py
    │   ├── grupo_sanguineo.py
    │   └── __init__.py      # importa todos los modelos y define Base.metadata
    └── main.py                 # Inicialización de FastAPI
├── .env
├── requirements.txt
├── .gitignore
└── README.md

