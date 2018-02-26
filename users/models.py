from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
import operator

from scorecards.models import Scorecard, Score

# One-to-One link extending the user class for adding additional data and functions
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def get_no_of_rounds(self):
        scorecards = self.user.scorecard_set.all()
        return len(scorecards)

    # Get average score on a specific round
    def get_round_average(self, course, round):
        scorecards = get_scorecards_by_round(self, round, course)

        for scorecard  in scorecards:
            total_score += scorecard.total_score

        average = total_score / len(scorecards)
        return average

    # Get the average score on a single hole
    def get_hole_average(self, course, hole):
        scorecards = Scorecard.objects.filter(course = course, user = self.user)

        scores = []
        total_score = 0

        for scorecard in scorecards:
            try:
                scores.append(scorecard.score_set.get(hole = hole)) # Unsure if this will work
            except Score.DoesNotExist:
                # No score at this round
                go = None

        for score in scores:
            total_score += score.score

        # Avoid div by 0
        if total_score > 0:
            average = total_score / len(scores)
        else:
            average = 0
        return average

# QUERY FUNCTIONS #

    # Get scorecards by given course
    def get_scorecards_by_course(self, course, order = None):
        if order is None:
            scorecards = Scorecard.objects.filter(course = course, user = self.user)
        else:
            scorecards = Scorecard.objects.filter(course = course, user = self.user).order_by(order)
        return scorecards

    # Get scorecards by given round
    def get_scorecards_by_round(self, round, course, order = None):
        if order is None:
            scorecards = Scorecard.objects.get(round = round, course = course, user = self.user)
        else:
            scorecards = Scorecard.objects.filter(round = round, course = course, user = self.user).order_by(order)
        return scorecards
    
    # Get the most played course for a user
    def get_most_played_course(self):
        scorecards = Scorecard.objects.filter(user = self.user)

        statistics = dict()
        
        # Generate a dict with all played courses, extracting this info from the scorecards
        for scorecard in scorecards:
            course = scorecard.course
            # If course has entry in dict, add one to that index
            if course.course_name in statistics:
                statistics[course.course_name] += 1
            # Else, create that dict position and set to 1
            else:
                statistics[course.course_name] = 1

        max_course = max(statistics.items(), key=operator.itemgetter(1))[0]
        times = statistics[max_course]
        return max_course, times

    # Get friends of user
    def friends(self):
        return Friendship.objects.filter(Q(creator = self.user) | Q(friend = self.user)).all() # Get friendships where user is creator OR friend

# USER LINKAGE FUNCTIONS #

# Create profile object that is related to a created user object
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save profile whenever the related user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Friendship model to model the friendship of two users
class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add = True, editable = False)
    creator = models.ForeignKey(User, related_name='friendship_creator_set')
    friend = models.ForeignKey(User, related_name='friend_set')