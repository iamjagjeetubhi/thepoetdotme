from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
#    url(r'^(?P<username>\w+)/$', views.myprofileview, name="detail_profile"),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^userpage/$', views.userpage, name='userpage'),
    url(r'^first_book/$', views.first_book, name='first_book'),
    url(r'^edit_profile/$', views.update_profile, name='update_profile'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login,name='login',
        kwargs={'redirect_authenticated_user': True, 'template_name': 'registration/login.html'}),
    url(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': 'login'}),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^change_password/$', views.change_password, name='change_password'),
]
