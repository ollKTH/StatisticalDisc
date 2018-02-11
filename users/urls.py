from django.conf.urls import url

from . import views


app_name = 'users'
urlpatterns = [
    # users/signup
    url(r'^signup/$', views.signup, name='signup'),

    # users/auth_user
    url(r'^auth_user', views.auth_user, name='auth_user'),

    # users/auth_user_logout
    url(r'^auth_user_logout', views.auth_user_logout, name='auth_user_logout')

    ]
