import csv
import os
from random import randint

from django.utils import timezone
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

from modelo.models import Persona, MovimientoPersona, Proyecto, CCT


class Command(BaseCommand):
    help = "Da de baja al personal no especificado en el CSV"
    c_new = 0
    p_new = 0

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        if options['filename'] == None:
            raise CommandError("Debe especificar la ruta al archivo CSV.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']):
            raise CommandError("El archivo especificado no existe.")
        activos = list()
        hoy = timezone.now()

        with open(options["filename"]) as f:
            dataReader = csv.reader(f, delimiter=',', quotechar='"')
            for row in dataReader:
                activos.append(row[3])

        for pers in Persona.objects.exclude(cuil__in=activos):
            MovimientoPersona.generar_baja(pers, hoy)
            self.c_new += 1

        self.stdout.write("Se dieron de baja {} personas.".format(self.c_new))
        self.c_new = 0
        myfile = open('no_encontradas.csv', 'w')
        wr = csv.writer(myfile)

        proyecto = Proyecto.objects.get(nombre='Sin proyecto')
        cct = CCT.objects.get(nombre__icontains="Fuera de convenio")

        with open(options["filename"]) as f:
            dataReader = csv.reader(f, delimiter=',', quotechar='"')
            for row in dataReader:
                self.fecha = datetime.strptime(row[4], "%d/%m/%Y")
                if not isinstance(self.fecha, datetime):
                    self.stdout.write("Fecha en formato erroneo. Saltando fila")
                    self.fecha = None
                if not Persona.all_persons.filter(cuil=row[3]).exists():
                    wr.writerow(row)
                    self.guardar_persona(row, cct, proyecto)
                    self.c_new += 1
        self.stdout.write("{} personas no encontradas. Se generó archivo no_encontradas.csv".format(self.c_new))
        myfile.close()

    def guardar_persona(self, row, cct, proyecto):
        persona = Persona()
        persona.legajo = randint(999999, 9999999)  # creo un número de legajo alto
        persona.apellido = ("{} {}".format(row[0], row[1])).strip()
        persona.nombre = row[2]
        persona.cuil = row[3]
        persona.cct = cct
        persona.proyecto = proyecto
        persona._history_date = self.fecha
        persona.save()
        self.p_new += 1
        self.stdout.write("Se creó nueva persona: {}.".format(str(persona)))
        return persona