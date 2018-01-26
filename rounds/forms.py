from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField

from .models import Round
from courses.models import Hole, Course

# Form to show when creating a round
class RoundForm(ModelForm):

    class Meta:
        model = Round
        fields = ['name', 'holes']

    # Pop with course
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course')
        
        super(RoundForm, self).__init__(*args, **kwargs)
        self.fields['holes'].widget = forms.CheckboxSelectMultiple()
        self.fields['holes'].queryset = course.hole_set.all()