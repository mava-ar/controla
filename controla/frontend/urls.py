from django.conf.urls import url

from frontend import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^asistencia/(?P<pk>\d+)/$', views.ver_asistencia, name="ver_asistencia"),
    url(r'^asistencia/(?P<pk>\d+)/alta/$', views.alta_asistencia, name="alta_asistencia"),
    url(r'^reasignar/$', views.reasignar_personal, name="reasignar_personal"),
]