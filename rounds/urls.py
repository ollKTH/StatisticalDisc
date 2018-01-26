from django.conf.urls import url

from . import views


app_name = 'rounds'
urlpatterns = [
    # rounds/createround/$
    url(r'^(?P<pk>\d+)/createround/$', views.createround, name='createround'),

    # rounds/rounddetails/5
    url(r'^rounddetails/(?P<pk>\d+)/$', views.rounddetails, name='rounddetails'),

    # rounds/rounddetails/5/rounddelete
    url(r'^rounddetails/(?P<pk>\d+)/rounddelete/$', views.rounddelete.as_view(), name='rounddelete'),
    ]