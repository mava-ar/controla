from django.conf.urls import url

from frontend.views import supervisor_views as views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^reasignar/$', views.reasignar_personal, name="reasignar_personal"),
]