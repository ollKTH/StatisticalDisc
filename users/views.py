from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from django_tables2 import RequestConfig
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout


from scorecards.models import Score, Scorecard
from scorecards.forms import ScoreForm
from courses.models import Course, Hole
from rounds.models import Round
from courses.forms import HoleForm
from rounds.forms import RoundForm
from courses.tables import CourseTable, HoleTable
from scorecards.tables import ScoreCardTable, ScoreTable
from rounds.tables import RoundTable

# Lets user sign up and create an account
def signup(request):
    # Create user
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Manual authentication of user
            
            # Redirect to index page
            courses = CourseTable(Course.objects.all())
            RequestConfig(request).configure(courses)
            return render(request, 'courses/index.html', {'courses': courses})
        # If something is not valid, post bound for with data and display errors
        else:
            context = {
            'form': form,
            }

            return render(request, 'users/signup.html', context)
    # Render user sign up form
    else:
        form = UserCreationForm()

        context = {
            'form': form,
            }

    return render(request, 'users/signup.html', context)

def auth_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)

            # Redirect user to start page
            courses = CourseTable(Course.objects.all())
            RequestConfig(request).configure(courses)
            return render(request, 'courses/index.html', {'courses': courses})
        else:
            raise NotImplementedError
    else:
        raise NotImplementedError

def auth_user_logout(request):
    logout(request)
    
    # Redirect user to start page
    courses = CourseTable(Course.objects.all())
    RequestConfig(request).configure(courses)
    return render(request, 'courses/index.html', {'courses': courses})