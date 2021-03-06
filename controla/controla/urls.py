"""controla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

from frontend.views.base import logout


urlpatterns = [
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/logout/', logout, name='logout'),
    url(r'^admin/login/$', views.login, {'template_name': 'auth/login.html'}, name='login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('frontend.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
