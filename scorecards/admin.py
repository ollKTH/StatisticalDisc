from django.contrib import admin

from .models import Score, Scorecard

class ScoreInLine(admin.TabularInline):
    model = Score
    extra = 18

class ScoreCardAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,      {'fields': ['course', 'date_played']}),
        ]
    inlines = [ScoreInLine]

admin.site.register(Scorecard, ScoreCardAdmin)
