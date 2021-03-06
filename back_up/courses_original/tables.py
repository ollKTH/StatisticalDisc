import django_tables2 as tables

from django_tables2.utils import A
from .models import Hole, Course, Scorecard, Score, Round

# TODO : Implement some styling highlightning the selected row from these tables

class CourseTable(tables.Table):
    course_name = tables.LinkColumn('courses:coursedetails', args=[A('pk')])

    class Meta:
        model = Course
        template = 'django_tables2/bootstrap.html'
        exclude = ('id')


class HoleTable(tables.Table):
    class Meta:
        model = Hole
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'course', 'scorecard')

class ScoreCardTable(tables.Table):
    course = tables.LinkColumn('courses:scorecarddetails', args=[A('pk')])

    class Meta:
        model = Scorecard
        template = 'django_tables2/bootstrap.html'
        exclude = ('id')

class ScoreTable(tables.Table):
    class Meta:
        model = Score
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'scorecard')

class RoundTable(tables.Table):
    name = tables.LinkColumn('courses:rounddetails', args=[A('pk')])

    class Meta:
        model = Round
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'course')
