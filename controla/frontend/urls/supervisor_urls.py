from django.conf.urls import url

from frontend.views import supervisor_views as views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^reasignar/$', views.reasignar_personal, name="reasignar_personal"),
    url(r'^personal/$', views.baja_personal, name="baja_personal"),
    url(r'^personal/(?P<pk>\d+)/$', views.ver_datos_persona, name="ver_datos_persona"),
    url(r'^datos_porcentuales/$', views.datos_porcentuales, name="datos_porcentuales"),
    url(r'^asistencia_estado/$', views.asistencia_persona, name="asistencia_estado"),
    url(r'^persona_proyecto/$', views.porcentaje_persona_proyecto, name="porcentaje_persona_proyecto"),
    url(r'^resumen_dias_trabajados/$', views.resumen_dias_trabajados, name="resumen_dias_trabajados"),

    url(r'^export_porcentual/$', views.export_porcentual, name="export_porcentual"),
    url(r'^export_asistencia/$', views.export_asistencia, name="export_asistencia"),
    url(r'^export_asistencia_cc/$', views.export_asistencia_cc, name="export_asistencia_cc"),
    url(r'^index_responsable/$', views.index_responsable, name="index_responsable"),
    url(r'^ver_proyectos/$', views.ver_proyectos_ajax, name="ver_proyectos_ajax"),
    url(r'^asistencia/(?P<pk>\d+)/$', views.ver_asistencia, name="ver_asistencia"),
    url(r'^asistencia/(?P<pk>\d+)/export2pdf$', views.export_asistencia_pdf, name="export_asistencia_pdf"),
    url(r'^asistencia/(?P<pk>\d+)/alta/$', views.alta_asistencia, name="alta_asistencia"),

    url(r'^notificaciones$', views.update_notification, name="update_notification"),
    url(r'^ver_asistencia$', views.ver_asistencia_fecha, name="ver_asistencia_fecha"),
    url(r'^ver_asistencia_ajax/$', views.ver_asistencia_ajax, name="ver_asistencia_ajax"),
    url(r'^fusionar_proyectos/$', views.fusionar_proyectos, name="fusionar_proyectos"),
    url(r'^proyecto/(?P<pk>\d+)/asistencia_del_dia$', views.asistencia_del_dia, name="asistencia_del_dia"),

]