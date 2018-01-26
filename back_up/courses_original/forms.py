from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField

from .models import Hole, Course, Scorecard, Score, Round

class HoleForm(ModelForm):
    class Meta:
        model = Hole
        fields = ['hole_number', 'hole_par', 'hole_length']

# This form remains unused, using template CreateView in views.py instead
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_par', 'course_location']

# To create a scorecard
class ScoreCardForm(ModelForm):
    class Meta:
        model = Scorecard
        fields = ['course', 'noOfHoles']

# To create a single score
class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'hole']

class RoundTestForm(ModelForm):
    class Meta:
        model = Round
        fields = ['name', 'holes', ]

# Form to show when creating a round
class RoundForm(ModelForm):

    class Meta:
        model = Round
        fields = ['name', 'holes']

    # Pop with course
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course')
        
        super(RoundForm, self).__init__(*args, **kwargs)
        #self.fields['holes'] = forms.ModelMultipleChoiceField(queryset = course.hole_set.all())
        self.fields['holes'].widget = forms.CheckboxSelectMultiple()
        self.fields['holes'].queryset = course.hole_set.all()




