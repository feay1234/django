from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from Lingo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^chat_list/$', views.chat_list, name='chat_list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

)
