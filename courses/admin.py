from django.contrib import admin

from .models import Course, Hole


class HoleInLine(admin.TabularInline):
    model = Hole
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,      {'fields': ['course_name', 'course_par', 'course_location']}),
        ]
    inlines = [HoleInLine]

admin.site.register(Course, CourseAdmin)