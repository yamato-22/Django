from django.contrib import admin
from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']
    list_filter = ['name']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject']

