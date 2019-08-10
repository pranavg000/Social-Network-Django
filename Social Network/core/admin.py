from django.contrib import admin
from .models import Profile,Following,Follower,Post,Comment

admin.site.register(Profile)
admin.site.register(Follower)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comment)

