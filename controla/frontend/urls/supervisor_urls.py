from django.conf.urls import url

from frontend.views import supervisor_views as views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^reasignar/$', views.reasignar_personal, name="reasignar_personal"),
    url(r'^datos_porcentuales/$', views.datos_porcentuales, name="datos_porcentuales"),
    url(r'^asistencia_persona/$', views.asistencia_persona, name="asistencia_persona"),
    url(r'^export_porcentual/$', views.export_porcentual, name="export_porcentual"),
    url(r'^export_asistencia/$', views.export_asistencia, name="export_asistencia"),
    url(r'^index_responsable/$', views.index_responsable, name="index_responsable"),
    url(r'^ver_proyectos/$', views.ver_proyectos_ajax, name="ver_proyectos_ajax"),
    url(r'^asistencia/(?P<pk>\d+)/$', views.ver_asistencia, name="ver_asistencia"),
    url(r'^asistencia/(?P<pk>\d+)/export2pdf$', views.export_asistencia_pdf, name="export_asistencia_pdf"),
    url(r'^asistencia/(?P<pk>\d+)/alta/$', views.alta_asistencia, name="alta_asistencia"),
]