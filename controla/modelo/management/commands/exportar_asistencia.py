import csv

from django.core.management.base import BaseCommand, CommandError

from modelo.models import Asistencia


class Command(BaseCommand):
    help = "Da de baja al personal no especificado en el CSV"
    c_new = 0
    p_new = 0

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        if options['filename'] == None:
            raise CommandError("Debe especificar la ruta al archivo CSV.")

        with open(options["filename"], 'w') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"')
            for asistencia in Asistencia.objects.all():
                row = ["{}".format(asistencia.fecha), asistencia.proyecto_id, ]
                # self.stdout.write("Asistencia de {} para {}".format(asistencia.fecha, asistencia.proyecto))
                for item in asistencia.items.all():
                    row.append("{}-{}".format(item.persona_id, item.estado_id))
                csv_writer.writerow(row)
