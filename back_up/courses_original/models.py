from django.db import models
from django.urls import reverse
from datetime import date


# Define the course model
class Course(models.Model):
    course_name = models.CharField(max_length=200) # Name of course
    course_par = models.PositiveIntegerField() # Course total par
    course_location = models.CharField(max_length=200) # Location, like town or such for the course

    def __str__(self):
        return self.course_name

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

# Round model, a defined round on a course with a number of holes. Makes the creation of scorecards easier(hopefully)
class Round(models.Model):
    name = models.CharField(max_length=200, null=True) # Name of round
    total_par = models.PositiveIntegerField(null = True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    holes = models.ManyToManyField(Hole)

    def get_total_par(self):
        for hole in self.holes.all(): # Will this work for M2M relation?
            total_par += hole.hole_par
        return total_par

    def get_absolute_url(self):
        return reverse('course:rounddetails', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.name)

# Define the Scorecard model, which has a course and can own several holes and scores
class Scorecard(models.Model):
    # TODO : Add user owner!

    round = models.ForeignKey(Round, on_delete=models.CASCADE, null = True) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True) # Foreign key for a scorecard is a single course
    date_played = models.DateField(default=date.today, null=True) # Date the scorecard was created
    noOfHoles = models.PositiveIntegerField(null = True) # Number of holes played on the card
    total_score = models.PositiveIntegerField(null = True) # Sum of all scores for a scorecard, can be set via get_total_score

    def get_absolute_url(self):
        return reverse('courses:scorecards')

    # Function to get the total score for a scorecard
    def get_total_score(self):
        total_score = 0
        for a_score in self.score_set.all():
            total_score += a_score.score

        return total_score

# DO WE NEED on_delete = CASCADE here? Will this delete all holes and such? How is the relationship?
    
# Define the Score model, which is just a value(score) on a hole represented in a scorecard
class Score(models.Model):
    score = models.PositiveIntegerField() # A score value for this score
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE) # A scorecard can own several scores
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE, blank=True, null=True) # A hole can have several scores for it