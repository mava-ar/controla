import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

from modelo.models import Estado, CCT, Persona, Proyecto, Asistencia, RegistroAsistencia


class Command(BaseCommand):
    help = "Realiza una importación de datos al sistema desde un CSV"
    p_new = 0
    a_new = 0
    r_new = 0

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        if options['filename'] == None:
            raise CommandError("Debe especificar la ruta al archivo CSV.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']):
            raise CommandError("El archivo especificado no existe.")
        import pdb; pdb.set_trace()  # XXX BREAKPOINT

        dataReader = csv.reader(open(options["filename"]), delimiter=',', quotechar='"')
        for row in dataReader:
            if row[0] != 'LEGAJO': # ignoramos la primera línea del archivo CSV
                pers_filt = Persona.objects.filter(legajo=row[0])
                proyecto = None
                if pers_filt:
                    persona = pers_filt[0]
                else:
                    # Si no existe la persona, quizás no existan las entidades
                    # relacionadas
                    cct, _ = CCT.objects.get_or_create(nombre=row[4])
                    proyecto, _ = Proyecto.objects.get_or_create(nombre=row[5])
                    proyecto = self.update_proyecto(proyecto, row)
                    persona = self.guardar_persona(row, cct, proyecto)
                # teniendo las entidades ya creadas, realizamos el
                # registro
                fecha = datetime.strptime(row[7], "%d/%m/%Y")
                if not isinstance(fecha, datetime):
                    self.stdout.write("Fecha en formato erroneo. Saltando fila")
                else:
                    if proyecto is None:
                        proyecto, _ = Proyecto.objects.get_or_create(nombre=row[5])
                        proyecto = self.update_proyecto(proyecto, row)
                    asistencia, is_new = Asistencia.objects.get_or_create(fecha=fecha, proyecto=proyecto)
                    if is_new:
                        asistencia.nombre_proyecto = proyecto.nombre
                        asistencia.nombre_responsable = str(proyecto.responsable)
                        asistencia.save()
                        self.a_new += 1
                    if not RegistroAsistencia.objects.filter(
                        asistencia=asistencia, persona=persona).exists():
                        registro = RegistroAsistencia(asistencia=asistencia, persona=persona)
                        estado, _ = Estado.objects.get_or_create(codigo=row[8])
                        registro.estado = estado
                        registro.codigo_estado = row[8]
                        registro.save()
                        self.r_new += 1

        self.stdout.write("Se han creado o actualizado {} persona, {} "
                          "asistencias con un total de {} registros.".format(
                              self.p_new, self.a_new, self.r_new))

    def guardar_persona(self, row, cct, proyecto):
        persona = Persona()
        persona.legajo = row[0]
        persona.apellido = row[1]
        persona.nombre = row[2]
        persona.cuil = row[3]
        persona.cct = cct
        persona.proyecto = proyecto
        persona.save()
        self.p_new += 1
        return persona

    def update_proyecto(self, proyecto, row):
        nom_list = row[6].split(' ')
        responsable = Persona.objects.filter(
            apellido__in=nom_list, nombre__in=nom_list)
        if responsable:
            proyecto.responsable = responsable[0]
            proyecto.save()
        return proyecto

