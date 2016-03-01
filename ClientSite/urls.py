'''
Author: Farmehr Farhour f.farhour@gmail.com
'''
from django.conf.urls import patterns, url
from ClientSite import views

urlpatterns = patterns('',
        url(r'^$', views.navigate, name='navigate'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^map/$', views.map, name='map'),
        url(r'^heatmap/$', views.heatmap, name='heatmap'),
        #url(r'^map/points', views.points, name='points'),
        )