from django.contrib import admin

from .models import Course, Hole, Scorecard, Score, Round


class HoleInLine(admin.TabularInline):
    model = Hole
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,      {'fields': ['course_name', 'course_par', 'course_location']}),
        ]
    inlines = [HoleInLine]

admin.site.register(Course, CourseAdmin)

class ScoreInLine(admin.TabularInline):
    model = Score
    extra = 18

class ScoreCardAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,      {'fields': ['course', 'date_played']}),
        ]
    inlines = [ScoreInLine]

admin.site.register(Scorecard, ScoreCardAdmin)

class RoundAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,     {'fields': ['name', 'course', 'total_par', 'holes']})
        ]

admin.site.register(Round, RoundAdmin)