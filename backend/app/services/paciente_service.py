from app.domain.models import Paciente, GrupoSanguineo
from app.domain.schemas import PacienteCreate, PacienteUpdate, PacienteRead
from app.repositories import PacienteRepository
from app.services import AlergiaService, AntecedenteService, GrupoSanguineoService, ObraSocialService

class PacienteService:
    def __init__(self, repository: PacienteRepository,
        alergia_service: AlergiaService,
        antecedente_service: AntecedenteService,
        grupo_sanguineo_service: GrupoSanguineoService,
        obra_social_service: ObraSocialService):
        self.repository = repository
        self.alergia_service = alergia_service
        self.antecedente_service = antecedente_service
        self.grupo_sanguineo_service = grupo_sanguineo_service
        self.obra_social_service = obra_social_service
    def obtener_todos(self) -> list[PacienteRead]:
        pacientes = self.repository.get_all()
        return [PacienteRead.model_validate(p) for p in pacientes]
    
    def obtener_por_id(self, id: int) -> PacienteRead | None:
        paciente = self.repository.get_by_id(id)
        if not paciente:
            raise ValueError(f"No se encontró el paciente con ID {id}.")
        return PacienteRead.model_validate(paciente)
    
    def crear_paciente(self, paciente_in: PacienteCreate) -> PacienteRead:
        datos_paciente = paciente_in.model_dump(exclude={"ids_alergias", "ids_antecedentes"})
        paciente = Paciente.model_validate(datos_paciente)

        if self.repository.get_by_dni(paciente.dni):
            raise ValueError(f"Ya existe un paciente con DNI {paciente.dni}.")
        
        if self.repository.get_by_email(paciente.email):
            raise ValueError(f"Ya existe un paciente con email {paciente.email}.")
        
        # Validar obra social
        if paciente_in.nombre_obra_social:
            obra_social = self.obra_social_service.obtener_modelo_por_nombre(paciente_in.nombre_obra_social)
            if not obra_social:
                raise ValueError(f"No se encontró la obra social con nombre {paciente_in.nombre_obra_social}.")
            paciente.obra_social = obra_social
        
        # validar grupo sanguineo
        if paciente_in.nombre_grupo_sanguineo:
            grupo_sanguineo = self.grupo_sanguineo_service.obtener_por_nombre(paciente_in.nombre_grupo_sanguineo)
            if not grupo_sanguineo:
                raise ValueError(f"No se encontró el grupo sanguíneo con nombre {paciente_in.nombre_grupo_sanguineo}.")
            paciente.grupo_sanguineo = grupo_sanguineo

        # Validamos y asignamos alergias
        if paciente_in.ids_alergias:
            alergias = []
            for alergia_id in paciente_in.ids_alergias:
                alergia = self.alergia_service.obtener_modelo_por_id(alergia_id)
                if not alergia:
                    raise ValueError(f"No se encontró la alergia con ID {alergia_id}.")
                alergias.append(alergia)
            paciente.alergias = alergias

        # Validamos y asignamos antecedentes
        if paciente_in.ids_antecedentes:
            antecedentes = []
            for antecedente_id in paciente_in.ids_antecedentes:
                antecedente = self.antecedente_service.obtener_modelo_por_id(antecedente_id)
                if not antecedente:
                    raise ValueError(f"No se encontró el antecedente con ID {antecedente_id}.")
                antecedentes.append(antecedente)
            paciente.antecedentes = antecedentes

        return PacienteRead.model_validate(self.repository.add(paciente))
    
    def actualizar(self, id: int, data: PacienteUpdate) -> Paciente | None:
        paciente_actual = self.repository.get_by_id(id)
        if not paciente_actual:
            raise ValueError(f"No se encontró el paciente con ID {id}.")
        
        if data.email and data.email != paciente_actual.email:
            if self.repository.get_by_email(data.email):
                raise ValueError(f"Ya existe un paciente con email {data.email}.")

        datos_simples = data.model_dump(
            exclude={"ids_alergias", "ids_antecedentes", "nombre_grupo_sanguineo", "nombre_obra_social"}, 
            exclude_unset=True
        )
        for key, value in datos_simples.items():
            if not hasattr(paciente_actual, key):
                raise ValueError(f"El atributo {key} no existe en Paciente.")
            setattr(paciente_actual, key, value)

        if data.nombre_obra_social is not None:
            obra_social = self.obra_social_service.obtener_modelo_por_nombre(data.nombre_obra_social)
            if not obra_social:
                raise ValueError(f"No se encontró la obra social con nombre {data.nombre_obra_social}.")
            paciente_actual.obra_social = obra_social
        
        if data.nombre_grupo_sanguineo is not None:
            grupo_sanguineo = self.grupo_sanguineo_service.obtener_por_nombre(data.nombre_grupo_sanguineo)
            if not grupo_sanguineo:
                raise ValueError(f"No se encontró el grupo sanguíneo con nombre {data.nombre_grupo_sanguineo}.")
            paciente_actual.grupo_sanguineo = grupo_sanguineo
        
        if data.ids_alergias is not None:
            nuevas_alergias = []
            for alergia_id in data.ids_alergias:
                alergia = self.alergia_service.obtener_modelo_por_id(alergia_id)
                if not alergia:
                    raise ValueError(f"No se encontró la alergia con ID {alergia_id}.")
                nuevas_alergias.append(alergia)
            paciente_actual.alergias = nuevas_alergias
        
        if data.ids_antecedentes is not None:
            nuevos_antecedentes = []
            for antecedente_id in data.ids_antecedentes:
                antecedente = self.antecedente_service.obtener_modelo_por_id(antecedente_id)
                if not antecedente:
                    raise ValueError(f"No se encontró el antecedente con ID {antecedente_id}.")
                nuevos_antecedentes.append(antecedente)
            paciente_actual.antecedentes = nuevos_antecedentes
        
        return self.repository.update(paciente_actual)
    
    def existe_paciente(self, dni: int) -> bool:
        paciente = self.repository.get_by_dni(dni)
        return paciente is not None