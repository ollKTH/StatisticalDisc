from django.shortcuts import render
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from django_tables2 import RequestConfig
from django.forms.models import modelformset_factory, formset_factory
import datetime

from .models import Score, Scorecard
from .forms import ScoreForm
from courses.models import Course, Hole
from rounds.models import Round
from courses.forms import HoleForm
from rounds.forms import RoundForm
from courses.tables import CourseTable, HoleTable
from scorecards.tables import ScoreCardTable, ScoreTable
from rounds.tables import RoundTable

# Render list of scorecards
def scorecards(request):
    table = ScoreCardTable(Scorecard.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'scorecards/scorecards.html', {'table': table})

# Details for a scorecard
def scorecarddetails(request, pk):
    scorecard = Scorecard.objects.get(id = pk)
    scores = ScoreTable(scorecard.score_set.all())
    RequestConfig(request).configure(scores)
    return render(request, 'scorecards/scorecarddetails.html', {'scores': scores, 'scorecard': scorecard})

def select_round(request, pk):
    if request.method == "POST":
        # THIS PART IS NOT USED, REDIRECTS TO FILL_SCORECARD WITH GET #

        course = request.POST.get('course')
        round_name = request.POST.get('selected_round') # Why does this return a string and not a Round object?

        # Get round and course
        course = Course.objects.get(course_name=course)
        round = Round.objects.get(name=round_name, course = course) # Okay get the actual round
        holes = round.holes.all()

        # Create Formset
        ScoreFormSet = modelformset_factory(Score, form = ScoreForm, fields = ('score',), extra = 0)
        score_formset = ScoreFormSet(queryset = holes)

        context = {
            'round': round,
            'course': course,
            'formset': score_formset,
            'holes': holes,
            }
        
        return render(request, 'scorecards/fill_scorecard.html', context)
    else:
        course = Course.objects.get(id = pk)
        rounds = course.round_set.all() # Get rounds for course
        context = {
            'rounds': rounds,
            'course': course
            }
        return render(request, 'scorecards/select_round.html', context)

def fill_scorecard(request):
    ScoreFormSet = modelformset_factory(Score, form = ScoreForm, fields = ('score',), extra = 0)
    if request.method == "POST":
        formset = ScoreFormSet(request.POST)
        course = Course.objects.get(course_name = request.POST.get('course')) # Get course
        round = Round.objects.get(name = request.POST.get('round'), course = course) # Get round
        holes = round.holes.all()

        i = 0
        total_score = 0
        scores = []

        # Loop over all forms in formset
        for form in formset:
            score = form.save(commit=False)
            score.hole = holes[i]
            total_score += score.score
            i += 1
            scores.append(score)

        # Create a scorecard object without scores
        scorecard = Scorecard(round = round, course = course, total_score = total_score, date_played = datetime.date.today(), noOfHoles = i)
        scorecard.save()

        # Assign each score to the scorecard
        for score in scores:
            score.scorecard = scorecard
            score.save()

        # For now just pass to index page
        courses = CourseTable(Course.objects.all())
        RequestConfig(request).configure(courses)
        return render(request, 'courses/index.html', {'courses': courses})
    else:
        course = request.POST.get('course')
        round_name = request.POST.get('selected_round') # Why does this return a string and not a Round object?

        # Get round and course
        course = Course.objects.get(course_name=course)
        round = Round.objects.get(name=round_name, course = course) # Okay get the actual round
        holes = round.holes.all()

        # Create Formset
        ScoreFormSet = modelformset_factory(Score, form = ScoreForm, fields = ('score',), extra = 0)
        score_formset = ScoreFormSet(queryset = holes)

        context = {
            'round': round,
            'course': course,
            'formset': score_formset,
            'holes': holes,
            }
        
        return render(request, 'scorecards/fill_scorecard.html', context)

