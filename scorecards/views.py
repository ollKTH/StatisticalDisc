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
from .tables import ScoreCardTable, ScoreTable, ScoreCardTableMini
from rounds.tables import RoundTable

# Render list of scorecards
def scorecards(request):
    scorecards = Scorecard.objects.filter(user = request.user)
    courses = Course.objects.all()

    return render(request, 'scorecards/scorecards.html', {'scorecards': scorecards, 'courses': courses})

# Details for a scorecard
def scorecarddetails(request, pk):
    scorecard = Scorecard.objects.get(id = pk)
    scores = Score.objects.filter(scorecard = scorecard)
    course = scorecard.course
    holes = scorecard.round.holes.all()

    context = {
               'scores': scores, 
               'scorecard': scorecard,
               'holes': holes,
               }
    return render(request, 'scorecards/scorecarddetails.html', context)

# Creating a scorecard without going from a course detailview, first #
# select course, then round #
def select_course(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            course_name = request.POST.get('selected_course')
            course = Course.objects.get(course_name = course_name)
            pk = course.pk
            return redirect('scorecards:select_round', pk = pk)
        else:
            courses = Course.objects.all()
            return render(request, 'scorecards/select_course.html', {'courses': courses})
    else:
        error = 'You have to log in before creating a scorecard!'
        return render(request, 'scorecards/error.html', {'error': error})


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
            user = request.user

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
            scorecard = Scorecard(round = round, course = course, total_score = total_score, date_played = datetime.date.today(), noOfHoles = i, user = user)
            scorecard.save()

            # Assign each score to the scorecard
            for score in scores:
                score.scorecard = scorecard
                score.save()

            # For now just pass to index page
            courses = CourseTable(Course.objects.all())
            RequestConfig(request).configure(courses)

            if request.user.is_authenticated:
                user = request.user

            noOfRounds = user.profile.get_no_of_rounds()
            scorecards = user.scorecard_set.order_by('-date_played')[0:4]
            most_played, times = user.profile.get_most_played_course()

            recent_scorecards = ScoreCardTableMini(scorecards)
            RequestConfig(request).configure(recent_scorecards)

            context = {'courses': courses, 
                       'noOfRounds': noOfRounds,
                       'recent_scorecards': recent_scorecards,
                       'most_played': most_played,
                       'times': times,
                       }
            return render(request, 'courses/index.html', context)
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


# Pick round for scorecard creation
def select_round(request, pk):
    if request.user.is_authenticated:
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
    else:
        error = 'You have to log in before creating a scorecard!'
        return render(request, 'scorecards/error.html', {'error': error})




