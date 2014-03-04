from django.conf.urls import patterns, url
from users import views


urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='auth'),
    url(r'^logout/$', views.logout_view, name='logout'),
)
