from django.contrib import admin
from Lingo.models import *

admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Language)
admin.site.register(Favorite)
admin.site.register(FriendInvitation)