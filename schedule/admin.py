from django.contrib import admin
from .models import *


class AdminEvent(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'date', 'current_class', 'room')
    list_display_links = ('current_class',)
    list_filter = ('current_class__type',)


admin.site.register(Schedule)
admin.site.register(Event, AdminEvent)