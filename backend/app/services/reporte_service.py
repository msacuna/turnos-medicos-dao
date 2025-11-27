from app.repositories import ReporteRepository
from app.domain.schemas import ReporteTurnoPorEspecialidad

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import Image


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

        # Crear gráficos de torta
        nombres_obras_sociales = [dato["obra_social"] for dato in datos]
        cantidades_afiliados = [dato["cantidad_pacientes"] for dato in datos]
        ingresos_totales = [dato["monto_total_turnos"] for dato in datos]

        # Filtrar datos para excluir obras sociales sin pacientes o ingresos
        nombres_obras_sociales_afiliados = [nombres_obras_sociales[i] for i in range(len(cantidades_afiliados)) if cantidades_afiliados[i] > 0]
        cantidades_afiliados_filtrados = [cantidad for cantidad in cantidades_afiliados if cantidad > 0]

        nombres_obras_sociales_ingresos = [nombres_obras_sociales[i] for i in range(len(ingresos_totales)) if ingresos_totales[i] > 0]
        ingresos_totales_filtrados = [ingreso for ingreso in ingresos_totales if ingreso > 0]

        # Gráfico de torta: Obra social por cantidad de afiliados
        buffer_afiliados = BytesIO()
        plt.figure(figsize=(6, 6))
        plt.pie(cantidades_afiliados_filtrados, labels=nombres_obras_sociales_afiliados, autopct='%1.1f%%', startangle=140)
        plt.title("Relación de Obras Sociales por Cantidad de Afiliados")
        plt.savefig(buffer_afiliados, format='png')
        plt.close()
        buffer_afiliados.seek(0)

        # Gráfico de torta: Obra social por ingresos
        buffer_ingresos = BytesIO()
        plt.figure(figsize=(6, 6))
        plt.pie(ingresos_totales_filtrados, labels=nombres_obras_sociales_ingresos, autopct='%1.1f%%', startangle=140)
        plt.title("Relación de Obras Sociales por Ingresos")
        plt.savefig(buffer_ingresos, format='png')
        plt.close()
        buffer_ingresos.seek(0)

        # Agregar gráficos al PDF
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("Gráfico: Relación de Obras Sociales por Cantidad de Afiliados", styles['Heading2']))
        elements.append(Image(buffer_afiliados, width=4 * inch, height=4 * inch))

        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("Gráfico: Relación de Obras Sociales por Ingresos", styles['Heading2']))
        elements.append(Image(buffer_ingresos, width=4 * inch, height=4 * inch))

        # Construir el PDF
        doc.build(elements)
        
        # Obtener la ruta absoluta del archivo PDF
        ruta_absoluta = os.path.abspath("../../reportes/reporte_pacientes_por_obra_social.pdf")

        # Devolver la ruta absoluta como respuesta
        return ruta_absoluta

    def reporte_profesionales_por_especialidad(self):
        resultados = self.repo.get_profesional_por_especialidad()
        
        if not resultados:
            raise Exception("No hay datos disponibles para generar el reporte.")

        # Verificar si la carpeta existe, si no, crearla
        self.verificar_o_crear_carpeta()

        doc = SimpleDocTemplate("../../reportes/profesionales_por_especialidad.pdf", pagesize=letter)

        elements = []
        styles = getSampleStyleSheet()

        # Título principal
        title = "Listado de profesionales según especialidad"
        elements.append(Paragraph(title, styles['Title']))

        # Párrafo introductorio
        intro = "Generación de listados por cada especialidad de los profesionales y la cantidad de dichos profesionales."
        elements.append(Paragraph(intro, styles['Normal']))
        elements.append(Spacer(1, 0.5 * inch))

        # Generar listas por especialidad
        for resultado in resultados:
            especialidad = resultado["especialidad"]
            cantidad_profesionales = resultado["cantidad_profesionales"]
            nombres_profesionales = resultado["nombres_profesionales"]

            # Título de la especialidad
            elements.append(Paragraph(f"Especialidad: {especialidad}", styles['Heading2']))
            elements.append(Paragraph(f"Cantidad de profesionales: {cantidad_profesionales}", styles['Normal']))

            # Lista de nombres de profesionales
            if nombres_profesionales:
                lista_nombres = nombres_profesionales.split(", ")
                for nombre in lista_nombres:
                    elements.append(Paragraph(f"- {nombre}", styles['Normal']))
            else:
                elements.append(Paragraph("No hay profesionales registrados para esta especialidad.", styles['Italic']))

            elements.append(Spacer(1, 0.1 * inch))  # Espaciado entre especialidades

        # Construir el PDF
        doc.build(elements)

        # Obtener la ruta absoluta del archivo PDF
        ruta_absoluta = os.path.abspath("../../reportes/profesionales_por_especialidad.pdf")

        # Devolver la ruta absoluta como respuesta
        return ruta_absoluta

    def verificar_o_crear_carpeta(self):
        carpeta_reportes = os.path.abspath("../../reportes")  # Ensure absolute path
        if not os.path.exists(carpeta_reportes):
            os.makedirs(carpeta_reportes)