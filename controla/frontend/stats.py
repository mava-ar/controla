import logging
from collections import defaultdict
from datetime import datetime, timedelta

from django.db.models import Count, Case, When

from modelo.models import Proyecto, RegistroAsistencia, Persona, Estado, Responsable

logger = logging.getLogger(__name__)


def get_proyectos_estados(hoy=None):
    if hoy is None:
        hoy = datetime.now()
    data = list(
        Proyecto.con_personas.annotate(
            ok=Count(Case(When(asistencias__fecha=hoy, then='asistencias__items__pk'))),
        ).values_list('pk', 'nombre', 'responsable_rel__persona__apellido',
                      'responsable_rel__persona__nombre', 'ok').order_by('-ok'))
    total = dict(Proyecto.con_personas.annotate(
        total=Count(Case(When(personas_involucradas__fecha_baja__isnull=True,
                              then='personas_involucradas__pk')))
        ).values_list('pk', 'total'))
    report = []
    for item in data:
        report.append(item + (total.get(item[0], 0),))
    return report


def porcentaje_asistencia_proyecto(hoy=None):
    if hoy is None:
        hoy = datetime.now()
    total = Proyecto.con_personas.count()

    perc = Proyecto.con_personas.filter(asistencias__fecha=hoy).count()
    # calculamos en el template
    # val = int(perc * 100 / total)
    # logger.debug("Total proyectos: {} | Proyecto con asistencias: {} | %: {}".format(total, perc, val))
    return total, perc


def porcentaje_actividad(hoy=None):
    if hoy is None:
        hoy = datetime.now()
    total = RegistroAsistencia.objects.filter(asistencia__fecha=hoy).count()
    if total == 0:
        return 0

    noociosos = RegistroAsistencia.objects.filter(asistencia__fecha=hoy, estado__no_ocioso=True).count()
    val = int(noociosos * 100 / total)
    logger.debug("Total asistencias: {} | Total no aciosos: {} | %: {}".format(total, noociosos, val))
    return "{}".format(val)


def porcentaje_asistencia_persona(hoy=None):
    if hoy is None:
        hoy = datetime.now()
    total = Persona.objects.filter(proyecto__isnull=False).count()

    registros = Persona.objects.filter(registro_asistencia__asistencia__fecha=hoy, proyecto__isnull=False).count()
    # calculamos en el template
    # val = int(registros * 100 / total)
    # logger.debug("Total personas: {} | Total registros hoy: {} | %: {}".format(total, registros, val))
    return total, registros # "{}".format(val)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield (start_date + timedelta(n)).date()


def sort_dict(adict, reverse=False):
    keys = adict.keys()
    keys = sorted(keys, reverse=reverse)
    return zip(keys, map(adict.get, keys))


def evolucion_registros_asistencia(start_date, ends_date):
    """
    Devuelve los datos para el gráfico de codigo de barras con los presentes y ausentes
    """
    qs = RegistroAsistencia.objects.select_related('estado', 'persona').filter(
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
            # desconozco porque debe sumar un día para que sea correcto el gráfico
            series["values"].append({'x': (day+ timedelta(days=1)).isoformat(), 'y': val})

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
        if total_rango == 0:
            totales_row.append(0)
        else:
            totales_row.append(totales_rango.get(est, 0) / total_rango)
    report.append(totales_row)

    for k,v in totales_rango.items():
        totales_rango[k] = v / total_rango * 100 if total_rango != 0 else 0
    return report, totales_rango


def get_asistencia_persona(start, end, group_by):
    """
    Reportes de cantidad de registros por estado por día, agrupados por group_by
    :param start: fecha limite inicial
    :param end: fecha limite final
    :param group_by: agrupador
    :return: reporte
    """
    if group_by is None:
        group_by = 'persona'
    processed = defaultdict(dict)
    header = list()
    estados = Estado.objects.values_list('codigo', flat=True)
    qs = RegistroAsistencia.objects.filter(
        asistencia__fecha__gte=start, asistencia__fecha__lte=end)
    if group_by == 'persona':
        qs = qs.values(
            'persona__apellido', 'persona__nombre', 'estado__codigo').annotate(cant=Count('pk')).order_by('persona')
        for it in qs:
            processed["{} {}".format(it["persona__apellido"], it["persona__nombre"])][it['estado__codigo']]=it["cant"]
        header.append("Nombre")
    elif group_by == 'responsable':
        qs = qs.values('asistencia__proyecto__responsable_rel__persona', 'estado__codigo').annotate(
            cant=Count('persona_id')).order_by('asistencia__proyecto__responsable_rel__persona__apellido')
        responsables = dict([(x[0], "{} {}".format(x[1], x[2])) for x in Responsable.objects.values_list(
            'persona', 'persona__apellido', 'persona__nombre').distinct()])

        for it in qs:
            processed[responsables[it["asistencia__proyecto__responsable_rel__persona"]]][it['estado__codigo']]=it["cant"]
        header.append("Responsable")

    report = list()
    header.extend(estados)
    header.append("Total")
    report.append(header)
    values = list()
    for nombre, data in sort_dict(processed):
        total_row = 0

        aux = list()
        aux.append(nombre)
        for est in estados:
            val = data.get(est, 0)
            aux.append(val)
            total_row += val
        aux.append(total_row)
        values.append(aux[1:])
        report.append(aux)
    totales = [sum(i) for i in zip(*values)]
    totales.insert(0, "Total general")
    report.append(totales)
    return report


def get_porcentaje_cc(start, end):
    """
    Muestra el porcentaje de asistencia por persona en cada proyecto
    :param start: fecha limite inicial
    :param end: fecha limite final
    :return: reporte
    """
    processed = defaultdict(dict)
    totales = dict()
    header = ["CCT", "APELLIDO NOMBRE", "C.U.I.L.", "PROYECTO", "Cuenta en ESTADO"]
    qs = RegistroAsistencia.objects.filter(
        asistencia__fecha__gte=start, asistencia__fecha__lte=end)
    qs = qs.values('persona__cct__nombre', 'persona__apellido','persona__nombre',
                   'persona__cuil', 'asistencia__proyecto__nombre',
                   ).annotate(est=Count('pk'))
    for it in qs:
        persona = "{} {}".format(it["persona__apellido"], it["persona__nombre"])
        processed[persona][it['asistencia__proyecto__nombre']]=it
        val = totales.get(persona, 0) + it["est"]
        totales[persona] = val

    report = list()
    report.append(header)

    for nombre, data in sort_dict(processed):
        for row, data1 in data.items():
            aux = list()
            porc = data1["est"] * 100 / totales.get(nombre)
            aux.extend([data1["persona__cct__nombre"], nombre, data1["persona__cuil"], row, "{0:.2f}".format(porc)])
            report.append(aux)
    return report
