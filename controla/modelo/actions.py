from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.utils import timezone
from django.contrib import messages
from django.utils.html import mark_safe


def dar_de_baja(modeladmin, request, queryset):

    if request.POST.get("post"):
        queryset.update(fecha_baja=timezone.now())

        message = mark_safe("Se dio la baja a las/os siguientes {}: {}".format(
                modeladmin.model._meta.verbose_name_plural,
                ', '.join(["<strong>{}</strong>".format(str(x)) for x in queryset])))
        messages.info(request, message)
    else:
        queryset1 = queryset.filter(fecha_baja=None)
        if queryset1:
            context = {
                "objects_name": modeladmin.model._meta.verbose_name_plural,
                'title': "Confirma la baja de {}".format(modeladmin.model._meta.verbose_name_plural),
                'baja_objects': queryset1,
                'ids': queryset1.values_list("id"),
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
            }
            return TemplateResponse(request, 'frontend/actions/confirm.html', context, current_app=modeladmin.admin_site.name)
        else:
            messages.warning(request, "No ha seleccionado {} activas/os".format(
                    modeladmin.model._meta.verbose_name_plural))