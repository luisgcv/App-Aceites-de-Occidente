from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, Image, PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from datetime import datetime
import tempfile
import webbrowser
from utils.rutas.rutas import obtener_ruta_recurso

import os

def exportar_pdf(datos, columnas, titulo):
    """Genera un PDF profesional con diseño mejorado."""
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        # Configuración de estilos
        estilos = getSampleStyleSheet()
        
        # Estilos personalizados
        estilo_titulo = ParagraphStyle(
            name="TituloPrincipal",
            parent=estilos["Title"],
            fontSize=16,
            textColor=colors.HexColor("#1A5276"),
            spaceAfter=12,
            alignment=1,
            fontName="Helvetica-Bold"
        )
        
        estilo_subtitulo = ParagraphStyle(
            name="Subtitulo",
            parent=estilos["Heading2"],
            fontSize=12,
            textColor=colors.HexColor("#2874A6"),
            spaceAfter=6,
            alignment=1
        )
        
        estilo_celda = ParagraphStyle(
            name="Celda",
            fontSize=9,
            leading=11,
            textColor=colors.black,
            fontName="Helvetica"
        )
        
        estilo_encabezado = ParagraphStyle(
            name="EncabezadoTabla",
            parent=estilo_celda,
            fontSize=10,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            alignment=1
        )

        # Configuración del documento
        doc = BaseDocTemplate(
            tmp.name,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=3*cm,
            bottomMargin=2.5*cm,
            title=titulo
        )

        # Marco principal
        frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width,
            doc.height,
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
            id='normal'
        )

        # Función para footer
        def footer(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.grey)
            
            # Línea decorativa
            canvas.setStrokeColor(colors.HexColor("#2874A6"))
            canvas.setLineWidth(0.5)
            canvas.line(doc.leftMargin, 2.2*cm, doc.width + doc.leftMargin, 2.2*cm)
            
            # Texto del footer
            footer_text = "© 2023 Aceites de Occidente y la Bajura - Todos los derechos reservados"
            canvas.drawCentredString(
                A4[0]/2.0,
                1.5*cm,
                footer_text
            )
            
            # Número de página
            canvas.drawRightString(
                doc.width + doc.leftMargin - 0.5*cm,
                1.5*cm,
                f"Página {doc.page}"
            )
            canvas.restoreState()

        # Plantilla con footer
        plantilla = PageTemplate(id='Principal', frames=frame, onPage=footer)
        doc.addPageTemplates([plantilla])

        # Construcción del contenido
        elementos = []

        # Logo (si existe)
        logo_path = obtener_ruta_recurso("app/utils/images/logo.jpg")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=6*cm, height=2.5*cm)
            logo.hAlign = 'CENTER'
            elementos.append(logo)
            elementos.append(Spacer(1, 0.5*cm))

        # Título principal
        elementos.append(Paragraph("Aceites de Occidente y la Bajura", estilo_subtitulo))
        elementos.append(Paragraph(titulo, estilo_titulo))
        
        # Fecha de generación
        fecha = Paragraph(
            f"<b>Generado:</b> {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
            ParagraphStyle(
                name="Fecha",
                fontSize=9,
                textColor=colors.grey,
                alignment=1
            )
        )
        elementos.append(fecha)
        elementos.append(Spacer(1, 1*cm))

        # Preparar datos para la tabla
        data = [[
            Paragraph(col, estilo_encabezado) for col in columnas
        ]] + [
            [
                Paragraph(str(item), estilo_celda) if isinstance(item, str) and len(item) > 30 else str(item)
                for item in row
            ]
            for row in datos
        ]

        ancho_util = A4[0] - doc.leftMargin - doc.rightMargin
        num_columnas = len(columnas)
        ancho_max_col = 7 * cm
        ancho_por_col = min(ancho_max_col, ancho_util / num_columnas)
        colWidths = [ancho_por_col] * num_columnas

        tabla = Table(
            data,
            colWidths=colWidths,
            repeatRows=1
        )

        # Estilo de la tabla
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2874A6")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8f9fa")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dee2e6")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 1*cm))

        # Generar PDF
        doc.build(elementos)
        webbrowser.open_new(tmp.name)

