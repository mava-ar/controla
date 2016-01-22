import csv
import os
from django.core.management.base import BaseCommand, CommandError

from modelo.models import Estado
from . import es_continuar


class Command(BaseCommand):
    help = "Importa los estados desde un CSV"
    c_new = 0

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        if options['filename'] == None:
            raise CommandError("Debe especificar la ruta al archivo CSV.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']):
            raise CommandError("El archivo especificado no existe.")

        dataReader = csv.reader(open(options["filename"]), delimiter=',', quotechar='"')
        for row in dataReader:
            if row[0] != 'SITUACIONES': # ignoramos la primera línea del archivo CSV
                estado, created = Estado.objects.get_or_create(codigo=row[1])
                if created:
                    self.guardar_estado(estado, row)
                else:
                    if estado.situacion == row[0] and estado.observaciones == row[2]:
                        # está todo igual, continuo
                        continue
                    else:
                        raw_value = input("El estado {} existe.\n"
                                          "Actual: {}. Obs: {}\nNuevo:  {}-{}. Obs: {}\n¿Desea reemplarlo (Y/n)? ".format(
                                                  estado.codigo, estado, estado.observaciones, row[1], row[0], row[2]))
                        if es_continuar(raw_value):
                            self.guardar_estado(estado, row)

        self.stdout.write("Se han creado o actualizado {} estados en el sistema.".format(self.c_new))

    def guardar_estado(self, estado, row):
        estado.situacion = row[0]
        estado.observaciones = row[2]
        estado.save()
        self.c_new += 1
