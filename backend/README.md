backend/
└── app/
    ├── api/ (aca van los diferentes endpoints + archivo main.py para enrutar)
    │   ├── routes/ (nuevamente las diferentes rutas -> archivos .py con endpoints)
    ├── services/        # Lógica de negocio / casos de uso
    │   ├── user_service.py
    │   ├── report_service.py
    ├── crud/            # Operaciones de BD puras (sería como los repositories)
    │   ├── user_crud.py
    │   ├── report_crud.py
    ├── schemas/ (modelos Pydantic, similar a DTOs)
    ├── core/ (configuracion y seguridad)
    │   ├── config.py    # Configuración de JWT, DB, etc.
    │   ├── security.py  # Funciones para JWT
    └── reports/
    │   ├── report_generator.py # Lógica para generar PDFs
    │   └── queries.py   # Consultas SQL específicas para reportes (opcional)
    ├── email_templates/ (formato en caso de hacer envio de mails)
    ├── models.py (definiciones de clases SQLAlchemy -> entidades)
    └── main.py (inicializar FastAPI)
├── .env
├── requirements.txt
├── .gitignore
└── README.md

