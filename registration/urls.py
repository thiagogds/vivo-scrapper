#coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('registration.views',
    url(r'^$', 'register', name='registration'),
    url(r'^register/complete$', 'registration_complete', name='registration_complete'),
    url(r'^activation/$', 'activation', name='activation'),
    url(r'^activation/complete/$', 'activation_complete', name='activation_complete'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(r'^login/$', 'login', name='login'),
)
