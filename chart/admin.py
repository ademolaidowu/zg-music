from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Track


class TrackAdmin(admin.ModelAdmin):

    actions = ['unchart', 'chart', 'accept', 'deny', 'reset_unirank', 'reset_zgmrank']
    def unchart(self, request, queryset):
        updated = queryset.update(status=0)
        self.message_user(request, ngettext(
            '%d track has been removed from the charts.',
            '%d tracks have been removed from the charts.',
            updated,
        ) % updated, messages.SUCCESS)

    unchart.short_description = "Remove selected tracks from charts"

    def chart(self, request, queryset):
        updated = queryset.update(status=1)
        self.message_user(request, ngettext(
            '%d track has been put on the charts.',
            '%d tracks have been put on the charts.',
            updated,
        ) % updated, messages.SUCCESS)

    chart.short_description = "Put selected tracks on charts"

    def accept(self, request, queryset):
        updated = queryset.update(submission=1)
        self.message_user(request, ngettext(
            '%d submitted track has been accepted.',
            '%d submitted tracks have been accepted.',
            updated,
        ) % updated, messages.SUCCESS)

    accept.short_description = "Accept selected track submission"

    def deny(self, request, queryset):
        updated = queryset.update(submission=2)
        self.message_user(request, ngettext(
            '%d submitted track has been denied.',
            '%d submitted tracks have been denied.',
            updated,
        ) % updated, messages.SUCCESS)

    deny.short_description = "Deny selected track submission"

    def reset_unirank(self, request, queryset):
        updated = queryset.update(uni_rank=None)
        self.message_user(request, ngettext(
            'The university rank of %d track has been reset.',
            'The university rank of %d tracks has been reset',
            updated,
        ) % updated, messages.SUCCESS)

    reset_unirank.short_description = "Reset university ranks"

    def reset_zgmrank(self, request, queryset):
        updated = queryset.update(zgm_rank=None)
        self.message_user(request, ngettext(
            'The zgm rank of %d track has been reset.',
            'The zgm rank of %d tracks has been reset',
            updated,
        ) % updated, messages.SUCCESS)

    reset_zgmrank.short_description = "Reset zgm ranks"


    list_display = ('title', 'artist', 'submission', 'status')
    list_filter = ('university', 'submission', 'status')
    search_fields = ['title', 'artist']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Track, TrackAdmin)