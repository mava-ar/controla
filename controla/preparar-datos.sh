#!/bin/bash

MIGR="../migracion"
# hacemos la carpeta que contendrá los archivos
mkdir $MIGR
# exportamos los datos de los usuarios
echo -n Exportando usuarios...
python manage.py exportar_usuarios $MIGR/usuarios.csv
echo OK
# exportamos los datos de organizacion a json
echo -n Exportando modelos para organizacion...
python manage.py dumpdata --indent 4 --natural-foreign --all modelo.Proyecto modelo.CCT modelo.Persona modelo.MovimientoPersona > $MIGR/organizacion.json
echo OK
# exportamos los datos de asistencia a json
echo -n Exportando modelos para asistencia...
python manage.py dumpdata --indent 4 --natural-foreign --all modelo.Estado modelo.responsable > $MIGR/asistencia.json
echo OK
# renombrar el nombre de la 
echo -n Renombrando json...
sed -i -- 's/modelo/organizacion/g' $MIGR/organizacion.json
# renombrar el nombre de la aplicacion
sed -i -- 's/modelo/asistencia/g' $MIGR/asistencia.json
sed -i -- 's/asistencia.estado/asistencia.estadoasistencia/g' $MIGR/asistencia.json
sed -i -- 's/asistencia.responsable/asistencia.responsableasistencia/g' $MIGR/asistencia.json
echo OK
# ejecutar command para extrar info de asistencia
echo -n Exportando datos de asistencia...
python manage.py exportar_asistencia $MIGR/asistencia.csv
echo OK!
