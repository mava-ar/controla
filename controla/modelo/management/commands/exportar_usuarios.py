import csv

from django.core.management.base import BaseCommand, CommandError

from users.models import User


class Command(BaseCommand):
    help = "Da de baja al personal no especificado en el CSV"
    c_new = 0
    p_new = 0

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        if options['filename'] is None:
            raise CommandError("Debe especificar la ruta al archivo CSV.")

        with open(options["filename"], 'w') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"')
            for user in User.objects.all():
                row = [user.pk, user.first_name, user.last_name, user.email, user.username, user.password,
                       user.is_superuser, user.is_staff, user.is_active, user.alertar_faltantes,
                       user.rol, user.notificar_alta_individual, user.notificar_alta_diario]
                csv_writer.writerow(row)