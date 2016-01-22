from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group as DjangoGroup

from users.models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {
            'fields': ('rol', 'cambia_personal', )
        }),
    ) + UserAdmin.fieldsets


admin.site.register(User, MyUserAdmin)
admin.site.unregister(DjangoGroup)
