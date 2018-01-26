from django.contrib import admin

from .models import Round

class RoundAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,     {'fields': ['name', 'course', 'total_par', 'holes']})
        ]

admin.site.register(Round, RoundAdmin)