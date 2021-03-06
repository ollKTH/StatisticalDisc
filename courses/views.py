from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from django_tables2 import RequestConfig

from .models import Course, Hole
from scorecards.models import Score, Scorecard
from rounds.models import Round
from .forms import HoleForm
from rounds.forms import RoundForm
from .tables import CourseTable, HoleTable
from scorecards.tables import ScoreCardTable, ScoreTable, ScoreCardTableMini
from rounds.tables import RoundTable

# TODO:
# ASANA : https://app.asana.com/0/507127549374093/board

# Course index view, presents list over courses available in db
def index(request):
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
        return render(request, 'courses/index.html', {'courses': courses})

# Rewritten course creator using Create-template out of Django
class coursecreate(generic.CreateView):
    model = Course
    template_name = 'courses/coursecreate.html'
    fields = ['course_name', 'course_location']
    
    # Set inital par to 0
    def form_valid(self, form):
        form.instance.course_par = 0 

        return super(coursecreate, self).form_valid(form)

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

# Create a course detail overview, showing holes and rounds
def coursedetails(request, pk):
    course = Course.objects.get(id=pk)
    holes = HoleTable(course.hole_set.all())
    rounds = RoundTable(course.round_set.all())
    context = {'holes': holes, 
               'course': course,
               'rounds': rounds,
               }
    RequestConfig(request, paginate={'per_page': 10}).configure(holes)
    return render(request, 'courses/coursedetails.html', context)

# When looking at coursedetails, user can add holes using this function. Checks if hole already exists so multiple holes doesnt get created
# THIS FUNCTION IS VERY STUPID!
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

            # Update course's total_par
            course.course_par = course.get_total_par()
            course.save()

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
    
# Javascript test page render
def javascript_test_page(request):
    return render(request, 'courses/Javascript_test/javascript_test_page.html')

# Hole details
def holedetails(request, pk):
    hole = Hole.objects.get(id = pk)
    course = Course.objects.get(course_name = hole.course)

    if request.user.is_authenticated:
        user = request.user
        average_score = request.user.profile.get_hole_average(course, hole)

        context = {
        'hole': hole,
        'course': course,
        'average': average_score,
            }

        return render(request, 'courses/holedetails.html', context)

    context = {
        'hole': hole,
        'course': course,
        }
    return render(request, 'courses/holedetails.html', context)