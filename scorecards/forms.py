from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField, BaseForm, Form
from django.forms.formsets import BaseFormSet

from .models import Scorecard, Score
from courses.models import Hole

class ScoreForm(Form):
    score = forms.IntegerField(min_value = 0)