from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


from dj_utils.pdf_utils import PdfPrint



class PdfPrintAltaAsistencia(PdfPrint):
    def report(self, asistencia, title):
        doc = SimpleDocTemplate(
            self.buffer,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72,
            pagesize=self.pageSize)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="TableHeader", fontSize=11, alignment=TA_CENTER,))
        styles.add(ParagraphStyle(
            name="ParagraphTitle", fontSize=11, alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(
            name="Justify", alignment=TA_JUSTIFY))
        # create document
        data = []
        data.append(Paragraph(title, styles['Title']))
        data.append(Paragraph("Proyecto: {0}".format(asistencia.proyecto), styles["Heading2"]))
        data.append(Paragraph("Responsable: {}".format(asistencia.proyecto.responsable_rel.persona), styles["Heading2"]))

        total = asistencia.items.count()
        presentes = asistencia.items.filter(estado__no_ocioso=True).count()
        prec_percentage = [presentes, (total-presentes), ]
        llabels = ['% presentes', '% ausentes', ]
        pie_chart = self.pie_chart_draw(prec_percentage, llabels)
        data.append(pie_chart)

        table_data = []
        # table header
        table_data.append([
            Paragraph('Nombre', styles['TableHeader']),
            Paragraph('Estado de asistencia', styles['TableHeader']),])
        for item in asistencia.items.all():
            table_data.append([
                item.persona,
                item.estado])
        wh_table = Table(table_data, colWidths=[doc.width/8.0*5, doc.width/8.0*3])
        wh_table.hAlign = 'LEFT'
        wh_table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        data.append(wh_table)

        doc.build(data, onFirstPage=self.pageNumber,
                  onLaterPages=self.pageNumber)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf

