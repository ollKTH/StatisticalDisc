import django_tables2 as tables

from django_tables2.utils import A
from .models import Scorecard, Score

# TODO : Implement some styling highlightning the selected row from these tables

class ScoreCardTable(tables.Table):
    course = tables.LinkColumn('scorecards:scorecarddetails', args=[A('pk')])

    class Meta:
        model = Scorecard
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'user', 'noOfHoles')

# Don't really know if used
class ScoreTable(tables.Table):
    class Meta:
        model = Score
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'scorecard')

# Mini version of the scorecard table
class ScoreCardTableMini(tables.Table):
    round = tables.LinkColumn('scorecards:scorecarddetails', args=[A('pk')])


    class Meta:
        model = Scorecard
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'date_played', 'noOfHoles', 'user')
        orderable = False
