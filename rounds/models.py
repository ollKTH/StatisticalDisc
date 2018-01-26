from django.db import models
from django.urls import reverse
from datetime import date
from django.db.models import Sum

# Round model, a defined round on a course with a number of holes. Makes the creation of scorecards easier(hopefully)
class Round(models.Model):
    name = models.CharField(max_length=200, null=True) # Name of round
    total_par = models.PositiveIntegerField(null = True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    holes = models.ManyToManyField('courses.Hole')

    # Get total par for a round
    def get_total_par(self):
        holes = Round.objects.get(id = self.id).holes.all()
        total_par = 0
        for hole in holes:
            total_par += hole.hole_par
        return total_par

    def get_absolute_url(self):
        return reverse('rounds:rounddetails', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.name)
