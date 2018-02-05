from django.conf.urls import url

from . import views

urlpatterns = [
    
    # scorecards/
    url(r'^$', views.scorecards, name='scorecards'),

    # scorecards/scorecarddetails/(?P<pk>\d+)/$
    url(r'^scorecarddetails/(?P<pk>\d+)/$', views.scorecarddetails, name='scorecarddetails'),

    # scorecards/select_round/$
    url(r'^(?P<pk>\d+)/select_round/$', views.select_round, name='select_round'),

    # scorecards/fill_scorecard/$
    url(r'^fill_scorecard/$', views.fill_scorecard, name='fill_scorecard'),

    # scorecards/select_course/$
    url(r'^select_course/$', views.select_course, name='select_course')
    ]
