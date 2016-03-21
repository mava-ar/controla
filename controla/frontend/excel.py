import io
import xlsxwriter


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
                'valign': 'vcenter'
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