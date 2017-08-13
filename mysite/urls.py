from django.conf.urls import include, url
from django.contrib import admin
# Static helper function only for development!
from django.conf.urls.static import static
from django.conf import settings
from accounts import views



from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^(?P<username>\w+)/$', views.myprofileview, name="myprofileview"),
    
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^avatar/', include('avatar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
