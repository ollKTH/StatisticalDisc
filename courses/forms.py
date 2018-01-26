from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField

from .models import Hole, Course
from rounds.models import Round

class HoleForm(ModelForm):
    class Meta:
        model = Hole
        fields = ['hole_number', 'hole_par', 'hole_length']

# This form remains unused, using template CreateView in views.py instead
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_par', 'course_location']

