from django.contrib import admin
from .models import *


class AdminSemester(admin.ModelAdmin):
    list_filter = ('year', 'type')


class AdminCourse(admin.ModelAdmin):
    list_display = ('title', 'year_group', 'semester', 'description')
    list_filter = ('semester__type', 'year_group__type')


admin.site.register(Semester, AdminSemester)
admin.site.register(Course, AdminCourse)
admin.site.register(ClassType)
admin.site.register(Class)
