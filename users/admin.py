from django.contrib import admin
from .models import *


class AdminYearGroup(admin.ModelAdmin):
    list_filter = ('type', 'year')


class AdminGroup(admin.ModelAdmin):
    list_filter = ('study_year__type', 'study_year__year')


admin.site.register(YearGroup, AdminYearGroup)
admin.site.register(Group, AdminGroup)
admin.site.register(User)
