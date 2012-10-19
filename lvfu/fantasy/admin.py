from django.contrib import admin

from models import Event, League


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'lv_id',
        'title',
        'description'
    )


class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'creation_time',
        'event',
        'title',
        'description'
    )
    date_hierarchy = 'creation_time'


admin.site.register(Event, EventAdmin)
admin.site.register(League, LeagueAdmin)
