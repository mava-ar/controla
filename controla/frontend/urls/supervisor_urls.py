from django.conf.urls import url

from frontend.views import supervisor_views as views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^reasignar/$', views.reasignar_personal, name="reasignar_personal"),
    url(r'^datos_porcentuales/$', views.datos_porcentuales, name="datos_porcentuales"),
    url(r'^asistencia_persona/$', views.asistencia_persona, name="asistencia_persona"),
    url(r'^export_porcentual/$', views.export_porcentual, name="export_porcentual"),
    url(r'^export_asistencia/$', views.export_asistencia, name="export_asistencia"),
]