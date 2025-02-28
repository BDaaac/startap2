from django.contrib import admin
from .models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'skill_level', 'directions', 'skills')
    search_fields = ('name', 'directions', 'skills')


admin.site.register(Teacher, TeacherAdmin)
