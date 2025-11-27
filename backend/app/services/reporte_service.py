from app.repositories import ReporteRepository
from app.domain.schemas import ReporteTurnoPorEspecialidad

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os


class ReporteService:
    def __init__(self, repo: ReporteRepository):
        self.repo = repo

    def reporte_turnos_especialidad(self) -> list[ReporteTurnoPorEspecialidad]:
        resultados = self.repo.get_turno_por_especialidad()
        reportes = [ReporteTurnoPorEspecialidad.model_validate(r) for r in resultados]
        return reportes
    

    def reporte_pacientes_por_obra_social(self):
        datos = self.repo.get_paciente_por_obra_social()

        if not datos:
            raise Exception("No hay datos disponibles para generar el reporte.")

        # Verificar si la carpeta existe, si no, crearla
        self.verificar_o_crear_carpeta()

        doc = SimpleDocTemplate("../../reportes/reporte_pacientes_por_obra_social.pdf", pagesize=letter)

        elements = []
        styles = getSampleStyleSheet()
        title = "Reporte de Pacientes por Obra Social"
        elements.append(Paragraph(title, styles['Title']))
        text = "Este informe presenta un resumen de las obras sociales, indicando la cantidad de afiliados de cada una y el ingreso total que han generado durante el período analizado."
        elements.append(Paragraph(text, styles['Normal']))

        # Crear tabla con los datos
        table_data = [["Obra Social", "Afiliados", "Monto"]]  # Cabecera de la tabla

        # Agregar filas con los datos
        for dato in datos:
            table_data.append([dato["obra_social"], dato["cantidad_pacientes"], f"${dato['monto_total_turnos']:.2f}"])

        # Crear tabla y aplicar estilo
        table = Table(table_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo gris para la cabecera
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para la cabecera
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar texto
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la cabecera
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en la cabecera
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para las filas
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Líneas de la tabla
        ]))

        # Agregar tabla a los elementos del PDF
        elements.append(Spacer(1, 0.5 * inch))  # Espaciado antes de la tabla
        elements.append(table)

        # Construir el PDF
        doc.build(elements)
        
        # Obtener la ruta absoluta del archivo PDF
        ruta_absoluta = os.path.abspath("../../reportes/reporte_pacientes_por_obra_social.pdf")

        # Devolver la ruta absoluta como respuesta
        return ruta_absoluta




    def verificar_o_crear_carpeta(self):
        carpeta_reportes = os.path.abspath("../../reportes")  # Ensure absolute path
        if not os.path.exists(carpeta_reportes):
            os.makedirs(carpeta_reportes)