from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from django_tables2 import RequestConfig

from .models import Course, Hole, Scorecard, Score, Round
from .forms import HoleForm, ScoreCardForm, ScoreForm, RoundForm, RoundTestForm
from .tables import CourseTable, HoleTable, ScoreCardTable, ScoreTable, RoundTable

# TODO:
# ASANA : https://app.asana.com/0/507127549374093/board

# Course index view, presents list over courses available in db
def index(request):
    courses = CourseTable(Course.objects.all())
    RequestConfig(request).configure(courses)
    return render(request, 'courses/index.html', {'courses': courses})

# Rewritten course creator using Create-template out of Django
class coursecreate(generic.CreateView):
    model = Course
    template_name = 'courses/coursecreate.html'
    fields = ['course_name', 'course_par', 'course_location']

# Let user edit course name, location and par
class courseedit(generic.UpdateView):
    model = Course
    fields = ['course_name', 'course_par', 'course_location']
    template_name = 'courses/courseedit.html'

# Let user delete course
class coursedelete(generic.DeleteView):
    model = Course
    template_name = 'courses/coursedelete.html'
    success_url = reverse_lazy('courses:index') # Go back to index view

# Create a course detail overview, showing holes and such
def coursedetails(request, pk):
    course = Course.objects.get(id=pk)
    holes = HoleTable(course.hole_set.all())
    rounds = RoundTable(course.round_set.all())
    context = {'holes': holes, 
               'course': course,
               'rounds': rounds,
               }
    RequestConfig(request).configure(holes)
    return render(request, 'courses/coursedetails.html', context)

# When looking at coursedetails, user can add holes using this function. Checks if hole already exists so multiple holes doesnt get created
def addhole(request, pk):
    if request.method == 'POST':
        course = Course.objects.get(id=pk)
        holeform = HoleForm(request.POST)
        new_hole = holeform.save(commit=False) # Create instance of object, DONT save to database
        new_hole.course_id = course.id
        check = 0;

        for hole in course.hole_set.all():
            if new_hole.hole_number == hole.hole_number: # Compare exisiting hole numbers to new one
                check = 1

        if check != 1: # If new hole, create and save
            new_hole.save()
            holetable = HoleTable(course.hole_set.all())
            form = HoleForm()
            context = {
                'hole': new_hole,
                'form': form,
                'holetable': holetable,
                'course': course,
            }
            return render(request, 'courses/addhole.html', context)
        elif check == 1:
            course = Course.objects.get(id=pk)
            holetable = HoleTable(course.hole_set.all())
            form = HoleForm()
            error = 'Hole already exists!' # Else return error string
            context = {
                    'course': course,
                    'form': form,
                    'error': error,
                    'holetable': holetable,
                }
            return render(request, 'courses/addhole.html', context)
    # If no POST, just return the view with course data
    else:
         course = Course.objects.get(id=pk)
         holetable = HoleTable(course.hole_set.all())
         form = HoleForm()
         context = {
                 'course': course,
                 'form': form,
                 'holetable': holetable,
                }
         return render(request, 'courses/addhole.html', context)

# Render list of courses
def courseoverview(request):
    table = CourseTable(Course.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'courses/courseoverview.html', {'table': table})

# Render list of scorecards
def scorecards(request):
    table = ScoreCardTable(Scorecard.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'courses/scorecards.html', {'table': table})

# Details for a scorecard
def scorecarddetails(request, pk):
    scorecard = Scorecard.objects.get(id = pk)
    scores = ScoreTable(scorecard.score_set.all())
    RequestConfig(request).configure(scores)
    return render(request, 'courses/scorecarddetails.html', {'scores': scores, 'scorecard': scorecard})

# Create Round with a number of holes, this will then be used for the scorecard
def createround(request, pk):
    if request.method == "POST":
        course = Course.objects.get(id=pk) # Get course
        form = RoundForm(request.POST, course = course)
        round = form.save(commit=False) # Create object, no save

        round.course = course # Might not be necessary if validiated in form?
        round.save()

        form.save_m2m() # As round object is saved, save m2m relationship

        round.total_par = round.get_total_par()
        round.save

        # Just for rendering coursedetails, instead => call coursedetails with pk
        holes = HoleTable(course.hole_set.all())
        rounds = RoundTable(course.round_set.all())
        context = {'holes': holes, 
                   'course': course,
                   'rounds': rounds,
                   }
        RequestConfig(request).configure(holes)
        return render(request, 'courses/coursedetails.html', context)
    else:
        course = Course.objects.get(id=pk)
        round_form = RoundForm(course = course)
        context = {
            'round_form': round_form,
            'course': course,
            }
        return render(request, 'courses/createround.html', context)
    
def rounddetails(request, pk):
    round = Round.objects.get(id = pk)
    hole_table = HoleTable(round.holes.all())
    context = {
        'round': round,
        'hole_table': hole_table,
        }
    return render(request, 'courses/rounddetails.html', context)
    