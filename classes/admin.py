from django.contrib import admin
from .models import *


class AdminSemester(admin.ModelAdmin):
    list_filter = ('type', 'year')


class AdminCourse(admin.ModelAdmin):
    list_display = ('title', 'year_group', 'semester', 'description')
    list_filter = ('semester__type', 'year_group__type')


class AdminClass(admin.ModelAdmin):
    list_display = ('type', 'course', 'teacher', 'per_week', '__groups__')
    list_display_links = ('course',)
    list_filter = ('type',)


admin.site.register(Semester, AdminSemester)
admin.site.register(Course, AdminCourse)
admin.site.register(ClassType)
admin.site.register(Class, AdminClass)
