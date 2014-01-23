from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from Lingo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^add_friend/$', views.add_friend, name='add_friend'),
    url(r'^accept_request/$', views.accept_request, name='accept_request'),
    url(r'^delete_friendInvitation/$', views.delete_friendInvitation, name='delete_friendInvitation'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^send_message', views.send_message, name='send_message'),
    url(r'^get_message', views.get_message, name='get_message'),
    url(r'^get_new_message', views.get_new_message, name='get_new_message'),
    url(r'^chat_list/$', views.chat_list, name='chat_list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^get_chat/$', views.get_chat, name='get_chat'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

)
