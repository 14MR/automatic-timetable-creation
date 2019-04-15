from django.contrib import admin
from .models import *


class AdminEvent(admin.ModelAdmin):
    list_display = ('timeslot', 'date', 'current_class', 'room')
    list_display_links = ('current_class',)
    list_filter = ('current_class__type',)


admin.site.register(Schedule)


class TimeslotAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'starting_time', 'ending_time')
    ordering = ('day_of_week', 'starting_time')


admin.site.register(Timeslot, TimeslotAdmin)
admin.site.register(Event, AdminEvent)
