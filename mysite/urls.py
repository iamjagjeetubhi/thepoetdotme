from django.conf.urls import include, url
from django.contrib import admin
# Static helper function only for development!
from django.conf.urls.static import static
from django.conf import settings
from accounts import views



from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^(?P<username>\w+)/$', views.myprofileview, name="myprofileview"),
    
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^avatar/', include('avatar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
