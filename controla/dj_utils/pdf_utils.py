from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .utils import get_random_colors, get_percentage


class PdfPrint:

    # initialize class
    def __init__(self, buffer, pageSize):
        self.buffer = buffer
        # default format is A4
        if pageSize == 'A4':
            self.pageSize = A4
        elif pageSize == 'Letter':
            self.pageSize = letter
        self.width, self.height = self.pageSize

    def pageNumber(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawCentredString(100*mm, 15*mm, str(number))

    def title_draw(self, x, y, text):
        chart_title = Label()
        chart_title.x = x
        chart_title.y = y
        # chart_title.fontName = 'FreeSansBold'
        chart_title.fontSize = 16
        chart_title.textAnchor = 'middle'
        chart_title.setText(text)
        return chart_title

    def legend_draw(self, labels, chart, **kwargs):
        legend = Legend()
        chart_type = kwargs['type']
        # legend.fontName = 'FreeSans'
        legend.fontSize = 13
        legend.strokeColor = None
        if 'x' in kwargs:
            legend.x = kwargs['x']
        if 'y' in kwargs:
            legend.y = kwargs['y']
        legend.alignment = 'right'
        if 'boxAnchor' in kwargs:
            legend.boxAnchor = kwargs['boxAnchor']
        if 'columnMaximum' in kwargs:
            legend.columnMaximum = kwargs['columnMaximum']
        # x-distance between neighbouring swatche\s
        legend.deltax = 0
        lcolors = get_random_colors(10)
        if chart_type == 'line':
            lcolors = [colors.red, colors.blue]
        elif chart_type == 'pie':
            lcolors = [colors.darkgreen, colors.darkblue] + lcolors
        legend.colorNamePairs = list(zip(lcolors, labels))

        for i, color in enumerate(lcolors):
            if chart_type == 'line':
                chart.lines[i].fillColor = color
            elif chart_type == 'pie':
                chart.slices[i].fillColor = color
            elif chart_type == 'bar':
                chart.bars[i].fillColor = color
        return legend

    def pie_chart_draw(self, values, llabels):
        d = Drawing(10, 150)
        # chart
        pc = Pie()
        pc.x = 50
        pc.y = 30
        # set data
        pc.data = values
        # set labels
        pc.labels = get_percentage(values)
        # set the link line between slice and it's label
        pc.sideLabels = 1
        # set width and color for slices
        pc.slices.strokeWidth = 1
        pc.slices.strokeColor = None
        d.add(self.title_draw(180, 140, 'Asistencia'))
        d.add(pc)
        d.add(self.legend_draw(llabels, pc, x=290, y=100, boxAnchor='ne',
                               columnMaximum=12, type='pie'))
        return d