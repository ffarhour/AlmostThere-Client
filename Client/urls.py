'''
Author: Farmehr Farhour f.farhour@gmail.com
'''
from django.conf.urls import patterns, include, url

#import views from ClientSite
from ClientSite import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Client.views.home', name='home'),
    # url(r'^Client/', include('Client.Client.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ClientSite/', include('ClientSite.urls')), 
    url(r'^$', views.index , name='index')
)
