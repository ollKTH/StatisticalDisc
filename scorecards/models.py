from django.db import models
from django.urls import reverse
from datetime import date

from courses.models import Course, Hole
from rounds.models import Round

# Define the Scorecard model, which has a course and can own several holes and scores
class Scorecard(models.Model):
    # TODO : Add user owner!

    round = models.ForeignKey('rounds.Round', on_delete=models.CASCADE, null = True) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True) # Foreign key for a scorecard is a single course
    date_played = models.DateField(default=date.today, null=True) # Date the scorecard was created
    noOfHoles = models.PositiveIntegerField(null = True) # Number of holes played on the card
    total_score = models.PositiveIntegerField(null = True) # Sum of all scores for a scorecard, can be set via get_total_score

    def get_absolute_url(self):
        return reverse('scorecards:scorecards')

    # Function to get the total score for a scorecard
    def get_total_score(self):
        total_score = 0
        for a_score in self.score_set.all():
            total_score += a_score.score
        return total_score

    # Function to get number of holes played on a scorecard
    def get_noOfHoles(self):
        noOfHoles = 0
        for round in self.round.holes.all():
            noOfHoles += 1
        return noOfHoles

    # Function to get total score, looping over all score objects
    def get_total_score(self):
        total_score = 0
        for score in self.score_set.all():
            total_score = score.score
        return total_score
    
# Define the Score model, which is just a value(score) on a hole represented in a scorecard
class Score(models.Model):
    score = models.PositiveIntegerField(null = True) # A score value for this score
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE, null = True) # A scorecard can own several scores
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE, blank=True, null=True) # A hole can have several scores for it
