from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group as DjangoGroup
from simple_history.admin import SimpleHistoryAdmin

from users.models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin, SimpleHistoryAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {
            'fields': ('rol', 'cambia_personal', 'notificar_alta_individual')
        }),
    ) + UserAdmin.fieldsets

    list_display = ('username', 'rol', 'email', 'first_name', 'last_name', 'is_staff',)


admin.site.register(User, MyUserAdmin)
admin.site.unregister(DjangoGroup)
