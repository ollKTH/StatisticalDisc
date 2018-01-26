import django_tables2 as tables

from django_tables2.utils import A
from .models import Round
from courses.models import Hole, Course

class RoundTable(tables.Table):
    name = tables.LinkColumn('rounds:rounddetails', args=[A('pk')])

    class Meta:
        model = Round
        template = 'django_tables2/bootstrap.html'
        exclude = ('id', 'course')