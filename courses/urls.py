from django.conf.urls import url

from . import views


app_name = 'courses'
urlpatterns = [
    # courses/
    url(r'^$', views.index, name='index'),
    
    # courses/coursecreate
    url(r'^coursecreate/$', views.coursecreate.as_view(), name='coursecreate'),

    # courses/coursedetails/5
    url(r'^coursedetails/(?P<pk>\d+)/$', views.coursedetails, name='coursedetails'),

    # courses/addhole
    url(r'^coursedetails/(?P<pk>\d+)/addhole/$', views.addhole, name='addhole'),

    # courses/courseedit/5
    url(r'^courseedit/(?P<pk>\d+)/$', views.courseedit.as_view(), name='courseedit'),

    # courses/coursedelete/5
    url(r'^coursedetails/(?P<pk>\d+)/coursedelete/$', views.coursedelete.as_view(), name='coursedelete'),

    # courses/coursedelete/5
    url(r'^courseoverview/$', views.courseoverview, name='courseoverview'),

    ]
