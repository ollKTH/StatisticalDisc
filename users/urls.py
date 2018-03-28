from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


app_name = 'users'
urlpatterns = [
    # users/signup
    url(r'^signup/$', views.signup, name='signup'),

    # users/auth_user
    url(r'^auth_user', views.auth_user, name='auth_user'),

    # users/auth_user_logout
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    #users/5/profile
    url(r'^(?P<pk>\d+)/profile/$', views.profile_page, name='profile'),

    # users/social
    url(r'^social/$', views.social, name='social'),

    # users/add_friend
    url(r'^add_friend/$', views.add_friend, name='add_friend'),

    ]
