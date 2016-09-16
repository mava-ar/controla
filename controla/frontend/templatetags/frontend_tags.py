from django.template.defaulttags import register
from frontend.stats import sort_dict


@register.filter
def get_persona(personas, form):
    try:
        if form.initial:
            return "{}".format(personas.get(form.initial["persona"]))
        else:
            return "{}".format(form.cleaned_data["persona"])
    except:
        return ""


@register.filter
def order_fecha_desc(datas):
    datas.sort(reverse=True)
    return datas


@register.filter
def percentage(data, num_decimal=1):
    try:
        return '{0:.{prec}f}'.format(data, prec=num_decimal)
    except:
        return ''


@register.filter
def hide_zero(data):
    if data == 0:
        return ''
    return data


@register.assignment_tag
def calc_porc_int(num, div):
    if div == 0:
        return "0"
    val = int(num * 100 / div)
    return str(val)