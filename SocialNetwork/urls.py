from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from core import views as user_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/',include('core.urls')),
    path('login/',auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
     path('welcome/',user_views.welcome,name="welcome"),
     path('logout/',auth_views.LogoutView.as_view(template_name='core/logout.html'),name='logout'),
     path('register/',user_views.UserFormView.as_view(template_name='core/registration_form.html'),name='register'),
     url(r'^profile/(?P<username>\w+)/$',user_views.profile,name='profile'),
     url(r'^followweb/(?P<username>\w+)/$',user_views.followweb,name="followweb"),
     url(r'^unfollowweb/(?P<username>\w+)/$',user_views.unfollowweb,name="unfollowweb"),
     url(r'^postweb/(?P<username>\w+)/$',user_views.postweb,name="postweb"),
     url(r'^commentweb/(?P<username>\w+)/(?P<post_id>\d+)/$', user_views.commentweb,name = "commentweb"),
     path('feed/',user_views.feed,name="feed"),
     
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)