import calendar
from collections import defaultdict
from datetime import datetime, timedelta

from django.db.models import Count

from modelo.models import Proyecto, RegistroAsistencia, Persona, Estado


def porcentaje_asistencia_proyecto(hoy=datetime.now()):
    total = Proyecto.objects.count()
    if total == 0:
        return 0

    perc = Proyecto.objects.filter(asistencias__fecha=hoy).count()
    return "{}".format(int(perc * 100 / total))


def porcentaje_actividad(hoy=datetime.now()):
    total = RegistroAsistencia.objects.filter(asistencia__fecha=hoy).count()
    if total == 0:
        return 0

    noociosos = RegistroAsistencia.objects.filter(asistencia__fecha=hoy, estado__no_ocioso=True).count()
    return "{}".format(int(noociosos * 100 / total))


def porcentaje_asistencia_persona(hoy=datetime.now()):
    total = Persona.objects.filter(proyecto__isnull=False).count()
    if total == 0:
        return 0

    registros = Persona.objects.filter(registro_asistencia__asistencia__fecha=hoy, proyecto__isnull=False).count()
    return "{}".format(int(registros * 100 / total))


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n)).date()


def sort_dict(adict, reverse=False):
    keys = adict.keys()
    keys = sorted(keys, reverse=reverse)
    return zip(keys, map(adict.get, keys))


def evolucion_registros_asistencia(start_date, ends_date):

    qs = RegistroAsistencia.objects.filter(
            asistencia__fecha__gte=start_date,
            asistencia__fecha__lte=ends_date).values_list(
            'asistencia__fecha', 'estado__no_ocioso').annotate(cant=Count('estado_id'))

    processed = defaultdict(dict)

    for it in qs:
        processed[it[0]][it[1]]=it[2]

    report = list()
    data_table = list()
    for day in daterange(start_date, ends_date + timedelta(days=1)):
        aux = list()
        aux.append(day)
        aux.append(processed.get(day, {}).get(True, 0))
        aux.append(processed.get(day, {}).get(False, 0))
        data_table.append(aux)

    for est in ["Presentes", "Ausentes"]:
        series = dict()
        series["key"] = est
        series["values"] = list()
        for day in daterange(start_date, ends_date + timedelta(days=1)):
            if est == "Presentes":
                val = processed.get(day, {}).get(True, 0)
            else:
                val = processed.get(day, {}).get(False, 0)
            series["values"].append({'x': day.isoformat(), 'y': val})

        report.append(series)

    return report, data_table


def evolucion_registros_x_estado(start_date, ends_date):
    estados = Estado.objects.values_list('codigo', flat=True)
    qs = RegistroAsistencia.objects.filter(
            asistencia__fecha__gte=start_date,
            asistencia__fecha__lte=ends_date).values_list(
            'asistencia__fecha', 'estado__codigo').annotate(cant=Count('estado_id'))

    processed = defaultdict(dict)
    esto = []
    for it in qs:
        processed[it[0]][it[1]]=it[2]
        if it[1] not in esto:
            esto.append(it[1])

    report = []
    for est in esto:
        series = {}
        series["key"] = est
        series["values"] = list()
        for day in daterange(start_date, ends_date + timedelta(days=1)):
            val = processed.get(day, {}).get(est, 0)
            series["values"].append({'x': day.isoformat(), 'y': val})

        report.append(series)

    return report


def get_datos_porcentuales(start, end):
    estados = Estado.objects.values_list('codigo', flat=True)
    qs = RegistroAsistencia.objects.filter(
        asistencia__fecha__gte=start,
        asistencia__fecha__lte=end
    ).values_list('asistencia__fecha', 'estado__codigo').annotate(cant=Count('pk')).order_by('asistencia__fecha')

    totales = dict(RegistroAsistencia.objects.filter(
        asistencia__fecha__gte=start,
        asistencia__fecha__lte=end
    ).values_list('asistencia__fecha').annotate(cant=Count('pk')).order_by('asistencia__fecha'))

    totales_rango = dict(RegistroAsistencia.objects.filter(
        asistencia__fecha__gte=start,
        asistencia__fecha__lte=end
    ).values_list('estado__codigo').annotate(cant=Count('pk')))
    total_rango = sum([v for k,v in totales_rango.items()])

    processed = defaultdict(dict)

    for it in qs:
        processed[it[0]][it[1]]=it[2]

    report = list()
    header = ["Fecha", ]
    header.extend(estados)
    report.append(header)

    totales_row = ["Totales", False,]

    for day in daterange(start, end + timedelta(days=1)):
        aux = list()
        aux.append(day)
        aux.append(day.isoweekday() in [6,7])
        data = processed.get(day, {})
        total = totales.get(day, 0)
        for est in estados:
            if total == 0:
                aux.append(0)
            else:
                aux.append(processed.get(day, {}).get(est, 0) * 100 / total)
        report.append(aux)

    for est in estados:
        totales_row.append(totales_rango.get(est, 0) / total_rango)
    report.append(totales_row)

    for k,v in totales_rango.items():
        totales_rango[k] = v / total_rango * 100
    return report, totales_rango


def get_asistencia_persona(start, end):
    estados = Estado.objects.values_list('codigo', flat=True)
    qs = RegistroAsistencia.objects.filter(
            asistencia__fecha__gte=start,
            asistencia__fecha__lte=end).values(
            'persona__apellido', 'persona__nombre', 'estado__codigo').annotate(cant=Count('pk'))

    processed = defaultdict(dict)
    for it in qs:
        processed["{} {}".format(it["persona__apellido"], it["persona__nombre"])][it['estado__codigo']]=it["cant"]

    report = list()
    header = ["Nombre", ]
    header.extend(estados)
    report.append(header)

    for nombre, data in processed.items():
        aux = list()
        aux.append(nombre)
        for est in estados:
            aux.append(data.get(est, ''))
        report.append(aux)

    return report
