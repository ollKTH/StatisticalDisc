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
from .tables import ScoreCardTable, ScoreTable
from rounds.tables import RoundTable

# Render list of scorecards
def scorecards(request):
    table = ScoreCardTable(Scorecard.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'scorecards/scorecards.html', {'table': table})

# Details for a scorecard
def scorecarddetails(request, pk):
    scorecard = Scorecard.objects.get(id = pk)
    scores = Score.objects.filter(scorecard = scorecard)
    course = scorecard.course
    holes = scorecard.round.holes.all()

    context = {'scores': scores, 
               'scorecard': scorecard,
               'holes': holes,

               }
    return render(request, 'scorecards/scorecarddetails.html', context)

# Pick round for scorecard creation
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
        ScoreFormSet = formset_factory(ScoreForm, extra = len(round.holes.all()))
        score_formset = ScoreFormSet()

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

# Fill out scorecard with POST data
def fill_scorecard(request):
    ScoreFormSet = formset_factory(ScoreForm)
    if request.method == "POST":
        # Create formset from the data available in the POST
        formset = ScoreFormSet(request.POST)
        if formset.is_valid():
            course = Course.objects.get(course_name = request.POST.get('course')) # Get course
            round = Round.objects.get(name = request.POST.get('round'), course = course) # Get round
            holes = round.holes.all()

            i = 0
            total_score = 0
            scores = []

            # Loop over all forms in formset
            for form in formset:
                score = Score()
                score.score = form.cleaned_data.get('score')
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
        ScoreFormSet = formset_factory(ScoreForm, fields = ('score',))
        score_formset = ScoreFormSet()

        context = {
            'round': round,
            'course': course,
            'formset': score_formset,
            'holes': holes,
            }
        
        return render(request, 'scorecards/fill_scorecard.html', context)

