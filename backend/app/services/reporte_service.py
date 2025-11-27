from app.repositories import ReporteRepository
from app.domain.schemas import ReporteCantidadTurnoPorEspecialidad, ReporteMontoTurnoPorEspecialidad

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import matplotlib
matplotlib.use('Agg')  # Usar backend 'Agg' para evitar problemas en entornos sin GUI
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import Image, PageBreak


class ReporteService:
    def __init__(self, repo: ReporteRepository):
        self.repo = repo

    def reporte_cantidad_turnos_especialidad(self):
        """
        Genera un PDF con el reporte de cantidad de turnos por especialidad (solo tabla)
        """
        resultados = self.repo.get_cantidad_turnos_por_especialidad()
        datos = [ReporteCantidadTurnoPorEspecialidad.model_validate(r) for r in resultados]

        if not datos:
            raise Exception("No hay datos disponibles para generar el reporte.")

        # Verificar si la carpeta existe, si no, crearla
        self.verificar_o_crear_carpeta()

        doc = SimpleDocTemplate("../../reportes/reporte_turnos_por_especialidad.pdf", pagesize=letter)

        elements = []
        styles = getSampleStyleSheet()
        title = "Reporte de Cantidad de Turnos por Especialidad"
        elements.append(Paragraph(title, styles['Title']))
        
        text = "Este informe presenta un resumen de las especialidades médicas, mostrando la cantidad de turnos registrados para cada una durante el período analizado."
        elements.append(Paragraph(text, styles['Normal']))

        # Crear tabla con los datos
        table_data = [["Especialidad", "Cantidad de Turnos"]]  # Cabecera de la tabla

        # Agregar filas con los datos
        total_turnos = 0
        for dato in datos:
            table_data.append([dato.especialidad, str(dato.cantidad_turnos)])
            total_turnos += dato.cantidad_turnos

        # Agregar fila de total
        table_data.append(["TOTAL", str(total_turnos)])

        # Crear tabla y aplicar estilo
        table = Table(table_data, colWidths=[4 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo gris para la cabecera
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para la cabecera
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar texto
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la cabecera
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en la cabecera
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),  # Fondo beige para las filas de datos
            ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey),  # Fondo gris claro para la fila total
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),  # Fuente en negrita para el total
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de la tabla
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical centrada
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ]))

        # Agregar tabla a los elementos del PDF
        elements.append(Spacer(1, 0.5 * inch))  # Espaciado antes de la tabla
        elements.append(table)

        # Agregar un resumen al final
        elements.append(Spacer(1, 0.5 * inch))
        summary_text = f"Resumen: Se registraron un total de {total_turnos} turnos distribuidos en {len(datos)} especialidades diferentes."
        elements.append(Paragraph(summary_text, styles['Normal']))

        # Construir el PDF
        doc.build(elements)
        
        # Obtener la ruta absoluta del archivo PDF
        ruta_absoluta = os.path.abspath("../../reportes/reporte_turnos_por_especialidad.pdf")

        # Devolver la ruta absoluta como respuesta
        return ruta_absoluta
    
    def reporte_montos_especialidad(self):
        resultados = self.repo.get_monto_turnos_por_especialidad()
        datos = [ReporteMontoTurnoPorEspecialidad.model_validate(r) for r in resultados]

        if not datos:
            raise Exception("No hay datos disponibles para generar el reporte.")

        # Verificar si la carpeta existe, si no, crearla
        self.verificar_o_crear_carpeta()

        doc = SimpleDocTemplate("../../reportes/reporte_montos_por_especialidad.pdf", pagesize=letter)

        elements = []
        styles = getSampleStyleSheet()
        title = "Reporte de Montos por Especialidad"
        elements.append(Paragraph(title, styles['Title']))
        
        text = "Este informe presenta un resumen de los montos totales generados por cada especialidad médica durante el período analizado."
        elements.append(Paragraph(text, styles['Normal']))

        # Crear tabla con los datos
        table_data = [["Especialidad", "Monto Total"]]  # Cabecera de la tabla

        # Agregar filas con los datos
        total_monto = 0.0
        for dato in datos:
            table_data.append([dato.especialidad, f"${dato.monto_total:.2f}"])
            total_monto += dato.monto_total

        # Agregar fila de total
        table_data.append(["TOTAL", f"${total_monto:.2f}"])

        # Crear tabla y aplicar estilo
        table = Table(table_data, colWidths=[4 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo gris para la cabecera
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para la cabecera
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar texto
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la cabecera
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en la cabecera
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),  # Fondo beige para las filas de datos
            ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey),  # Fondo gris claro para la fila total
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),  # Fuente en negrita para el total
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de la tabla
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical centrada
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ]))

        # Agregar tabla a los elementos del PDF
        elements.append(Spacer(1, 0.5 * inch))  # Espaciado antes de la tabla
        elements.append(table)

        # Agregar un resumen al final
        elements.append(Spacer(1, 0.5 * inch))
        summary_text = f"Resumen: Se generó un monto total de ${total_monto:.2f} distribuido en {len(datos)} especialidades diferentes."
        elements.append(Paragraph(summary_text, styles['Normal']))

        # Construir el PDF
        doc.build(elements)
        
        # Obtener la ruta absoluta del archivo PDF
        ruta_absoluta = os.path.abspath("../../reportes/reporte_montos_por_especialidad.pdf")

        # Devolver la ruta absoluta como respuesta
        return ruta_absoluta
    
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
    
    def generar_reporte_periodo(self, mes_inicio: int, mes_fin: int, anio: int):
        """
        Genera un PDF con el reporte de turnos por período usando directamente los datos del repositorio
        """
        # 1. Obtener datos del repositorio
        datos_crudos = self.repo.get_turnos_por_periodo(mes_inicio, mes_fin, anio)
        
        # 2. Obtener datos mensuales para el gráfico (EXPLÍCITAMENTE ESTE MÉTODO)
        datos_mensuales = self.repo.get_turnos_por_periodo_mensual(mes_inicio, mes_fin, anio)
        
        if not datos_crudos:
            raise Exception("No hay datos disponibles para generar el reporte.")

        # 3. Calcular totales directamente de los datos crudos
        total_turnos = sum(fila['cantidad'] for fila in datos_crudos)
        total_ingresos = sum(float(fila['monto_estimado']) for fila in datos_crudos)

        # 4. Crear PDF
        self.verificar_o_crear_carpeta()
        doc = SimpleDocTemplate(f"../../reportes/reporte_turnos_periodo_{anio}_{mes_inicio}_{mes_fin}.pdf", pagesize=letter)

        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title = f"Reporte de Turnos - Período {mes_inicio}/{anio} a {mes_fin}/{anio}"
        elements.append(Paragraph(title, styles['Title']))
        
        # Descripción
        text = f"Este informe presenta un análisis detallado de los turnos médicos durante el período comprendido entre {mes_inicio}/{anio} y {mes_fin}/{anio}, mostrando la distribución por estados y evolución mensual."
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))

        # 5. Crear tabla usando directamente datos_crudos
        table_data = [["Estado", "Cantidad de Turnos", "Monto Estimado"]]
        
        for fila in datos_crudos:
            # También aseguramos float aquí para el formateo
            monto = float(fila['monto_estimado'])
            table_data.append([
                fila['estado'],
                str(fila['cantidad']),
                f"${monto:.2f}"
            ])
        
        # Fila de totales
        table_data.append(["TOTAL", str(total_turnos), f"${total_ingresos:.2f}"])

        # Estilo de tabla
        table = Table(table_data, colWidths=[2.5 * inch, 2 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.5 * inch))

        # 6. GRÁFICO DE LÍNEAS - EJE X DINÁMICO SEGÚN EL RANGO CONSULTADO
        if datos_mensuales:
            # Extraer todos los estados únicos de los datos mensuales
            todos_los_estados = sorted(set([d['estado'] for d in datos_mensuales]))
            
            # EJE X DINÁMICO: del mes_inicio al mes_fin
            meses_rango = list(range(mes_inicio, mes_fin + 1))
            
            # Organizar datos: para cada estado, obtener cantidad por mes en el rango
            datos_grafico = {}
            for estado in todos_los_estados:
                datos_grafico[estado] = []
                for mes in meses_rango:
                    # Buscar la cantidad para este estado en este mes específico
                    cantidad = 0
                    for registro in datos_mensuales:
                        if registro['estado'] == estado and int(registro['mes']) == mes:
                            cantidad = registro['cantidad']
                            break
                    datos_grafico[estado].append(cantidad)

            # Crear gráfico
            buffer_grafico = BytesIO()
            plt.figure(figsize=(12, 7))
            
            # Colores distintivos para cada estado
            colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            
            # Crear una línea para cada estado
            for i, estado in enumerate(todos_los_estados):
                color = colores[i % len(colores)]
                plt.plot(meses_rango, datos_grafico[estado], 
                        marker='o', label=estado, color=color, 
                        linewidth=2, markersize=6)
            
            # Configurar gráfico
            plt.title(f"Evolución de Turnos por Estado ({mes_inicio}/{anio} - {mes_fin}/{anio})", 
                    fontsize=14, fontweight='bold')
            plt.xlabel("Mes", fontsize=12)
            plt.ylabel("Cantidad de Turnos", fontsize=12)
            
            # Eje X dinámico: según el rango consultado
            plt.xticks(meses_rango, [f'{m}' for m in meses_rango])
            plt.xlim(mes_inicio - 0.5, mes_fin + 0.5)
            
            # Eje Y: comenzar desde 0
            plt.ylim(bottom=0)
            
            # Leyenda y grilla
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            
            # Agregar valores en los puntos (solo donde hay datos > 0)
            for estado in todos_los_estados:
                for j, mes in enumerate(meses_rango):
                    cantidad = datos_grafico[estado][j]
                    if cantidad > 0:
                        plt.annotate(str(cantidad), (mes, cantidad), 
                                textcoords="offset points", xytext=(0,10), 
                                ha='center', fontsize=8)
            
            plt.tight_layout()
            plt.savefig(buffer_grafico, format='png', bbox_inches='tight', dpi=150)
            plt.close()
            buffer_grafico.seek(0)

            # Forzar salto de página antes del gráfico
            elements.append(PageBreak())

            # Agregar gráfico al PDF
            elements.append(Paragraph(f"Evolución Mensual por Estado (Meses {mes_inicio}-{mes_fin})", styles['Heading2']))
            elements.append(Image(buffer_grafico, width=8 * inch, height=5.6 * inch))
            elements.append(Spacer(1, 0.3 * inch))

        # 7. Agregar resumen final
        num_meses = mes_fin - mes_inicio + 1
        num_estados = len(datos_crudos)
        resumen = f"Resumen del período: Se registraron {total_turnos} turnos con un monto total estimado de ${total_ingresos:.2f}, distribuidos en {num_estados} estados diferentes durante {num_meses} mes(es)."
        elements.append(Paragraph(resumen, styles['Normal']))

        # 8. Construir PDF
        doc.build(elements)
        
        ruta_absoluta = os.path.abspath(f"../../reportes/reporte_turnos_periodo_{anio}_{mes_inicio}_{mes_fin}.pdf")
        return ruta_absoluta