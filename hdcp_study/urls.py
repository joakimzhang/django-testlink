"""hdcp_study URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import settings
import django

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(
        'hdcp_app.urls', namespace='hdcp_app', app_name='hdcp_app')),
    url(r'', include('Ts_app.urls', namespace='Ts_app', app_name='Ts_app')),
    #url(r'^media/(?P<path>.*)$', django.views.static.serve,{'document_root':settings.MEDIA_ROOT}),
    #url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':'/home/anna/Documents/django_py/showImg/image/pic'}),
]
