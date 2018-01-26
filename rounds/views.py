from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from django_tables2 import RequestConfig

from .models import Round
from courses.models import Course, Hole
from .forms import RoundForm
from courses.forms import HoleForm
from .tables import RoundTable
from courses.tables import CourseTable, HoleTable

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
        round.save()

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
        return render(request, 'rounds/createround.html', context)
    
def rounddetails(request, pk):
    round = Round.objects.get(id = pk)
    hole_table = HoleTable(round.holes.all())
    context = {
        'round': round,
        'hole_table': hole_table,
        }
    return render(request, 'rounds/rounddetails.html', context)

class rounddelete(generic.DeleteView):
    model = Round
    template_name = 'rounds/rounddelete.html'
    success_url = reverse_lazy('courses:index') # Go back to index view
