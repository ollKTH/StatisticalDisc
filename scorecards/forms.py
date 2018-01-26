from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms.formsets import BaseFormSet

from .models import Scorecard, Score
from courses.models import Hole

class ScoreForm(ModelForm):
    class Meta:
        fields = ['score', 'hole']



    # Let's initiate each scoreform with a hole
    #def __init__(self, *args, **kwargs):
        #hole_id = kwargs.pop('hole')
        #super(ScoreForm, self).__init__(*args, **kwargs)

        #self.fields['hole'] = Hole.objects.get(id = hole_id)
