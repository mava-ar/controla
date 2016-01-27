from django.template.defaulttags import register


@register.filter
def get_persona(personas, form):
    try:
        if form.initial:
            return "{}".format(personas.get(form.initial["persona"]))
        else:
            return "{}".format(form.cleaned_data["persona"])
    except:
        return ""
