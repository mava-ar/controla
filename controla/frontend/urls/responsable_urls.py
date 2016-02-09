from django.conf.urls import url

from frontend.views import responsable_views as views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^asistencia/(?P<pk>\d+)/$', views.ver_asistencia, name="ver_asistencia"),
    url(r'^asistencia/(?P<pk>\d+)/alta/$', views.alta_asistencia, name="alta_asistencia"),
    url(r'^reasignar/$', views.reasignar_personal, name="reasignar_personal"),
    url(r'^notificaciones$', views.update_notification, name="update_notification"),
    url(r'^ver_asistencia$', views.ver_asistencia_fecha, name="ver_asistencia_fecha"),
    url(r'^ver_asistencia_ajax/$', views.ver_asistencia_ajax, name="ver_asistencia_ajax"),
]