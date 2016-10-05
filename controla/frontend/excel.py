import io
import os
import xlsxwriter
from datetime import datetime
from collections import Counter

from django.conf import settings

from modelo.models import Estado
from dj_utils.dates import daterange


class ExportExcelMixin:
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def get_c(self, col):
        """ Convert given row and column number to an Excel-style cell name. """
        result = []
        while col:
            col, rem = divmod(col-1, 26)
            result[:0] = self.LETTERS[rem]
        return ''.join(result)

    def __init__(self):
        self.output = io.BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output, {'in_memory': True})
        self.set_default_style()

    def prepare_response(self):
        self.workbook.close()
        xlsx_data = self.output.getvalue()
        # xlsx_data contains the Excel file
        return xlsx_data

    def set_default_style(self):
        self.style_dict = {
            'title': self.workbook.add_format({
                'bold': True,
                'font_size': 14,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'header': self.workbook.add_format({
                'bg_color': '#59677e',
                'color': 'white',
                'align': 'left',
                'valign': 'vcenter',
                'border': 1,
                'bold': True,
                'font_size': 12,
            }),
            'header_num': self.workbook.add_format({
                'bg_color': '#59677e',
                'color': 'white',
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'bold': True,
                'font_size': 12,
                'num_format': '$ #,##0.00'
            }),
            'header_perc': self.workbook.add_format({
                'bg_color': '#59677e',
                'color': 'white',
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'bold': True,
                'font_size': 12,
                'num_format': '0.0%'
            }),
            'header_date': self.workbook.add_format({
                'bg_color': '#59677e',
                'color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'bold': True,
                'font_size': 12,
                'num_format': 'dd/mm/yy'
            }),
            'normal': self.workbook.add_format({
                'color': 'black',
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
            }),
            'normal_money': self.workbook.add_format({
                'color': 'black',
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '$ #,##0.00'
            }),
            'normal_date': self.workbook.add_format({
                'color': 'black',
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'num_format': 'dd/mm/yy'
            }),
            'normal_perc': self.workbook.add_format({
                'color': 'black',
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '0.0%'
            }),
            'total': self.workbook.add_format({
                'color': 'red',
                'bg_color': 'yellow',
                'align': 'left',
                'valign': 'vcenter',
                'border': 2,
                'num_format': '$ #,##0.00'
            }),
            'total_legend': self.workbook.add_format({
                'color': 'red',
                'bg_color': 'yellow',
                'align': 'right',
                'valign': 'vcenter',
                'border': 2,
            }),
        }


class ExportToExcel(ExportExcelMixin):

    def fill_datos_porcentuales(self, context):
        """
        Este reporte muestra el porcentaje de cada estado de asistencia, por día.

        """
        worksheet_s_name = "Datos exportados"
        worksheet_s = self.workbook.add_worksheet(worksheet_s_name)
        row = 0
        for item in context["table"]:
            if row == 0:
                worksheet_s.write_row(row, 0, item, self.style_dict["header"])
            else:
                worksheet_s.write(row, 0, item[0], self.style_dict["header"] if item[0] == "Totales" else self.style_dict["normal_date"])

                it = 1
                for x in item[2:]:
                    worksheet_s.write(
                            row, it, x/100, self.style_dict["header_perc"] if item[0] == "Totales" else self.style_dict["normal_perc"])
                    it += 1
            row += 1
        worksheet_s.autofilter('A1:A1')
        worksheet_s.freeze_panes(1, 1)
        return self.prepare_response()

    def fill_asistencia_x_estado(self, context):
        """
        Este reporte muestra la cantidad de dias con cada estado por persona, para el rango de fechas dadas.
        """
        worksheet_s_name = "Datos exportados"
        worksheet_s = self.workbook.add_worksheet(worksheet_s_name)
        row = 0
        for item in context["table"]:
            if row == 0:
                worksheet_s.write_row(row, 0, item, self.style_dict["header"])
            else:
                it = 1
                worksheet_s.write(row, 0, item[0], self.style_dict["header"])
                for x in item[1:]:
                    worksheet_s.write(
                            row, it, x if x else None, self.style_dict["normal"])
                    it += 1
            row += 1
        worksheet_s.set_column(0, 0, 40)
        worksheet_s.autofilter('A1:A1')
        worksheet_s.freeze_panes(1, 1)
        return self.prepare_response()

    def fill_asistencia_proyecto(self, context):
        """
        Este reporte muestra el porcentaje de afectación de cada persona a un proyecto, dentro del rango de fechas dadas.
        """
        worksheet_s_name = "Datos exportados"
        worksheet_s = self.workbook.add_worksheet(worksheet_s_name)
        row = 0
        for item in context["table"]:
            if row == 0:
                worksheet_s.write_row(row, 0, item, self.style_dict["header"])
            else:
                it = 0
                for x in item:

                    try:
                        cal = float(x)
                    except:
                        cal = 0
                    worksheet_s.write(
                            row, it, cal/100 if it == 4 else x , self.style_dict["normal_perc"] if it == 4 else self.style_dict["normal"])
                    it += 1
            row += 1
        worksheet_s.set_column(0, 4, 25)
        worksheet_s.autofilter('A1:E1')
        worksheet_s.freeze_panes(1, 1)
        return self.prepare_response()

    def fill_resumen_dias_trabajados(self, context):
        """
        Muestra un reporte de con el detalle de asistencia cada dia (dentro del rango de fechas)
        por persona para un proyecto seleccionado.
        """
        worksheet_s_name = "Resumen RRHH"
        worksheet_s = self.workbook.add_worksheet(worksheet_s_name)
        fechas = context["filter"].form.cleaned_data["fecha"]
        start_date = fechas.start
        end_date = fechas.stop
        rango_de_dias = [x for x in daterange(start_date, end_date)]

        # cabecera con logo y título "Resumen de días trabajados" - RRHH -
        # subcabecera: fecha de emisión y proyecto seleccionado
        # referencia de estados y códigos
        # encabezado de tabla
        """
        Resumen personal    | Días              | * cada estado con su acumulado
        personas            | Cada dia          | Acumulado por persona por estado
        ...
        * Total cada estado | Acumulado diario  | Totales

        """

        # formats
        header = self.workbook.add_format({
            'color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'bold': True,
            'font_size': 12,
        })
        header_date = self.workbook.add_format({
            'color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'bold': True,
            'font_size': 12,
            'num_format': 'dd/mm/yy'
        })

        normal = self.workbook.add_format({
            'color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 9,
        })
        normal_color = self.workbook.add_format({
            'bg_color': '#b6eda8',
            'color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 9,
        })

        xs_total_color = self.workbook.add_format({
            'bg_color': '#c6a5a5',
            'color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 9,
        })
        cant_dias = len(rango_de_dias)
        # título
        worksheet_s.merge_range(0, 0, 0, 3, "")
        worksheet_s.insert_image(0, 0, os.path.join(settings.STATIC_ROOT, "frontend/img/footer-zille.png"),
                                 {'x_offset': 15, 'y_offset': 5})
        worksheet_s.merge_range(0, 4, 0, cant_dias + 3, "RESUMEN DE DÍAS TRABAJADOS\n-RRHH-", self.style_dict["title"])

        # subtítulo
        worksheet_s.merge_range(1, 0, 1, 1, "Fecha de Emisión:", header)
        worksheet_s.merge_range(1, 2, 1, 3, datetime.now(), header_date)

        worksheet_s.merge_range(1, 4, 1, 14, "Operación (Proyecto / Servicio):", header)
        worksheet_s.merge_range(1, 15, 1, 3 + cant_dias,
                                str(context["filter"].form.cleaned_data["proyecto"]), header)

        referencias = dict(Estado.objects.values_list("codigo", "situacion"))

        # mejorar presentación de referencias..
        # worksheet_s.write(2, 0, " ".join(["REFERENCIAS: ", ] + referencias))

        # encabezados tabla
        worksheet_s.merge_range(3 , 0, 3, 3, "RESUMEN PERSONAL DE ZILLE SRL", normal_color)
        worksheet_s.merge_range(3, 4, 3, cant_dias + 3, "MES", normal_color)

        # encabezados
        worksheet_s.write_row(4, 0, ["ITEM", "APELLIDO Y NOMBRE", "CUIL", "CATEGORÍA"], normal_color)
        worksheet_s.write_row(4, 4, [x.strftime("%d/%m") for x in rango_de_dias], normal_color)

        # encabecados estados
        i = 4
        for k, v in referencias.items():
            worksheet_s.merge_range(3, cant_dias + i, 4, cant_dias + i, "{}\n{}".format(k, v), xs_total_color)
            i += 1

        # buscamos las personas, las ordenamos por apellido
        personas = context["filter"].qs.values_list(
            'persona_id', 'persona__apellido', 'persona__nombre', 'persona__cuil').order_by(
            "persona__apellido", "persona__nombre").distinct()

        row_init_data = item = 5  # primer fila con datos

        totales_diarios = {}  # dict con una lista de asistencias por día. Key: dia, value, list de estados
        totales_por_estados = {}

        for persona in personas:
            # datos de empleado
            worksheet_s.write_row(item, 0, [
                item-4,  # item
                "{}, {}".format(persona[1], persona[2]),  # nombre
                persona[3],  # cuit
                ""  # categoria
            ], normal)
            col = 4  # columna de datos de asistencia
            avance = 0  # avance de la columna
            asistencia = dict(context["filter"].qs.filter(
                persona_id=persona[0]).values_list(
                "asistencia__fecha", 'estado__codigo').order_by("asistencia__fecha"))
            totales = Counter(asistencia.values())

            # guardos los totales de esta persona, para calcular los totales por estado
            for k, total in totales.items():
                try:
                    totales_por_estados[k].append(total)
                except KeyError:
                    totales_por_estados[k] = [total, ]

            # recorremos los días
            for dia in rango_de_dias:
                # armo dict para contabilizar asistencias por día
                if dia not in totales_diarios:
                    totales_diarios[dia] = []
                totales_diarios[dia].append(asistencia.get(dia, ""))

                worksheet_s.write(item, col + avance, asistencia.get(dia, ""), normal)
                avance += 1

            # poner campos para estados y sus sumatorias
            for estado in referencias.keys():
                worksheet_s.write_formula(item, col + avance,
                                          '=COUNTIF({0}{1}:{2}{1},"{3}")'.format(
                                              self.get_c(col + 1),
                                              item + 1,
                                              self.get_c(col + avance),
                                              estado),
                                          cell_format=xs_total_color,
                                          value=totales.get(estado, 0))
                avance += 1
            item += 1

        row_fin_data = item - 1
        # lista de estados y totales diarios
        for estado in referencias.keys():
            col = 4  # columna de datos de asistencia
            avance = 0  # avance de la columna
            worksheet_s.merge_range(item, 0, item, 3, "TOTAL {}".format(referencias.get(estado)), xs_total_color)
            # recorremos los días
            for dia in rango_de_dias:
                totales_dia = Counter(totales_diarios.get(dia, []))
                worksheet_s.write_formula(item, col + avance,
                                          '=COUNTIF({0}{1}:{0}{2},"{3}")'.format(
                                              self.get_c(col + avance + 1),
                                              row_init_data + 1,
                                              row_fin_data + 1,
                                              estado),
                                          cell_format=xs_total_color,
                                          value=totales_dia.get(estado, 0))
                avance += 1
            if item == row_fin_data + 1:  # si es el primero de los totales, agrego los totales por estado

                for estado2 in referencias.keys():
                    total = sum(totales_por_estados.get(estado2, []))
                    # primero hago el merge de la celda
                    worksheet_s.merge_range(item, col + avance, item + 3, col + avance, "")
                    # luego aplico la formula
                    worksheet_s.write_formula(
                        item, col + avance,
                        '=SUM({0}{1}:{0}{2})'.format(self.get_c(col + avance + 1), row_init_data + 1, row_fin_data + 1),
                        cell_format=normal_color, value=total)

                    avance += 1

            item += 1

        # setear altos y  anchos
        worksheet_s.set_row(0, 45)
        worksheet_s.set_row(1, 30)
        worksheet_s.set_column(0, 0, 5)
        worksheet_s.set_column(1, 1, 40)
        worksheet_s.set_column(2, 2, 15)
        worksheet_s.set_column(3, 3, 10)
        worksheet_s.set_column(4, 4 + cant_dias, 5)
        worksheet_s.freeze_panes(5, 2)
        return self.prepare_response()
