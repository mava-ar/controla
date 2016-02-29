import csv
import os
from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from modelo.models import Estado, CCT, Persona, Proyecto, Asistencia, RegistroAsistencia, Responsable


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

        dataReader = csv.reader(open(options["filename"]), delimiter=',', quotechar='"')
        for row in dataReader:
            if row[0] != 'LEGAJO': # ignoramos la primera línea del archivo CSV
                self.fecha = datetime.strptime(row[7], "%d/%m/%Y")
                if not isinstance(self.fecha, datetime):
                    self.stdout.write("Fecha en formato erroneo. Saltando fila")
                    self.fecha = None
                    continue
                self.fecha = timezone.make_aware(self.fecha)
                if not row[0].strip() == '':
                    pers_filt = Persona.all_persons.filter(legajo=row[0])
                else:
                    pers_filt = Persona.all_persons.filter(cuil=row[3])
                proyecto = None
                if pers_filt:
                    persona = pers_filt[0]
                else:
                    # Si no existe la persona, quizás no existan las entidades
                    # relacionadas
                    try:
                        cct = CCT.objects.get(nombre=row[4])
                    except CCT.DoesNotExist:
                        if row[4].strip() == '':
                            cct = CCT.objects.get(nombre__icontains="Fuera de convenio")
                        else:
                            cct = CCT(nombre=row[4])
                            cct._history_date = self.fecha
                            cct.save()
                            self.stdout.write("Se creó nuevo CCT {}.".format(cct.nombre))
                    proyecto = self.get_proyecto_or_default(row[5], row)
                    persona = self.guardar_persona(row, cct, proyecto)
                # teniendo las entidades ya creadas, realizamos el
                # registro

                if proyecto is None:
                    proyecto = self.get_proyecto_or_default(row[5], row)
                try:
                    asistencia = Asistencia.objects.get(fecha=self.fecha, proyecto=proyecto)
                except Asistencia.DoesNotExist:
                    asistencia = Asistencia(fecha=self.fecha, proyecto=proyecto, nombre_responsable=row[6])
                    asistencia._history_date = self.fecha
                    asistencia.save()
                    self.a_new += 1
                if not RegistroAsistencia.objects.filter(
                    asistencia=asistencia, persona=persona).exists():
                    registro = RegistroAsistencia(asistencia=asistencia, persona=persona)
                    estado = self.get_estado_or_default(codigo=row[8])
                    registro.estado = estado
                    if estado.codigo != row[8]:
                        registro.observaciones = "Código original en la planilla {}".format(row[8])
                    registro._history_date = self.fecha
                    registro.save()
                    self.r_new += 1
                    # self.stdout.write("Registro creado -> {}".format(registro))

        self.stdout.write("Se han creado o actualizado {} persona, {} "
                          "asistencias con un total de {} registros.".format(
                              self.p_new, self.a_new, self.r_new))

    def guardar_persona(self, row, cct, proyecto):
        persona = Persona()
        persona.legajo = row[0] if row[0] else row[3].replace('-','')
        persona.apellido = row[1]
        persona.nombre = row[2]
        persona.cuil = row[3]
        persona.cct = cct
        persona.proyecto = proyecto
        persona._history_date = self.fecha
        persona.save()
        self.p_new += 1
        self.stdout.write("Se creó nuevo persona {}.".format(str(persona)))
        return persona

    def buscar_responsable(self, proyecto, row):
        nom_list = row[6].split(' ')
        if nom_list[0].startswith("Olivo"):
            nom_list[0] = "Olivo"
        persona = Persona.all_persons.filter(
            apellido=nom_list[0], nombre__icontains=nom_list[1])
        if persona:
            try:
                responsable = Responsable.objects.get(proyecto=proyecto)
                if responsable.persona != persona[0]:
                    responsable.persona = persona[0]
                    responsable._history_date = self.fecha
                    responsable.save()
            except Responsable.DoesNotExist:
                responsable = Responsable(persona=persona[0], proyecto=proyecto)
                responsable._history_date = self.fecha
                responsable.save()
                self.stdout.write("Se asignó responsable -> {}.".format(str(responsable)))

    def get_proyecto_or_default(self, nombre, row):
        if nombre.strip() == '':
            p = Proyecto.objects.get(nombre="Sin proyecto")
            return p
        else:
            try:
                p = Proyecto.all_proyects.get(nombre=nombre.strip())
            except Proyecto.DoesNotExist:
                p = Proyecto(nombre=nombre.strip())
                p._history_date = self.fecha
                p.save()
                self.stdout.write("Se creó nuevo proyecto {}.".format(p.nombre))
            self.buscar_responsable(p, row)
            return p

    def get_estado_or_default(self, codigo):
        try:
            est = Estado.objects.get(codigo=codigo)
            return est
        except Estado.DoesNotExist:
            est = Estado.objects.get(codigo="SD")
            return est