import django_tables2 as tables

from django_tables2.utils import A
from .models import Scorecard, Score

# TODO : Implement some styling highlightning the selected row from these tables

class ScoreCardTable(tables.Table):
    course = tables.LinkColumn('scorecarddetails', args=[A('pk')])

    class Meta:
        model = Scorecard
        template = 'django_tables2/bootstrap.html'
        exclude = ('id')

class ScoreTable(tables.Table):
    class Meta:
        model = Score
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'scorecard')