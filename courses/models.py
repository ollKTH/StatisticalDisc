from django.db import models
from django.urls import reverse
from datetime import date


# Define the course model
class Course(models.Model):
    course_name = models.CharField(max_length=200) # Name of course
    course_par = models.PositiveIntegerField(null=True) # Course total par
    course_location = models.CharField(max_length=200) # Location, like town or such for the course

    def __str__(self):
        return self.course_name

    def get_total_par(self):
        total_par = 0
        holes = self.hole_set.all()
        if holes:
            for hole in holes:
                total_par += hole.hole_par
            return total_par
        else:
            return total_par

    def get_absolute_url(self):
        return reverse('courses:coursedetails', kwargs={'pk': self.pk})

# Define the hole model
class Hole(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # Foreign key for a hole is a single course
    hole_number = models.PositiveIntegerField() # Hole number on the course
    hole_par = models.PositiveIntegerField() # Hole par
    hole_length = models.PositiveIntegerField() # Hole length in meters

    def __str__(self):
        return str(self.course)+ ", Hole: " + str(self.hole_number) # Display course and hole number

    def __unicode__(self):
        return str(self.hole_number)