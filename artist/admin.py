from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Artist, ArtistCategory


class ArtistAdmin(admin.ModelAdmin):
    actions = ['paid', 'unpaid', 'verify', 'confirm', 'deny', 'graduate', 'send_confirmation', 'send_rejection']

    def paid(self, request, queryset):
        updated = queryset.update(paid=True)
        self.message_user(request, ngettext(
            '%d artist payment has been verified.',
            '%d artist payments have been verified.',
            updated,
        ) % updated, messages.SUCCESS)

    paid.short_description = "Verify payment for selected artists"


    def unpaid(self, request, queryset):
        updated = queryset.update(paid=False)
        self.message_user(request, ngettext(
            '%d artist payment has been cancelled.',
            '%d artist payments have been cancelled.',
            updated,
        ) % updated, messages.SUCCESS)

    unpaid.short_description = "Cancel payment for selected artists"


    def verify(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, ngettext(
            '%d artist has been verified.',
            '%d artists have been verified.',
            updated,
        ) % updated, messages.SUCCESS)

    verify.short_description = "Verify selected artists"


    def confirm(self, request, queryset):
        updated = queryset.update(status=1)
        self.message_user(request, ngettext(
            '%d artist application has been confirmed.',
            '%d artist applications has been confirmed.',
            updated,
        ) % updated, messages.SUCCESS)

    confirm.short_description = "Confirm artist application"


    def deny(self, request, queryset):
        updated = queryset.update(status=2)
        self.message_user(request, ngettext(
            '%d artist application has been denied.',
            '%d artist applications has been denied.',
            updated,
        ) % updated, messages.SUCCESS)

    deny.short_description = "Deny artist application"


    def graduate(self, request, queryset):
        updated = queryset.update(status=3)
        self.message_user(request, ngettext(
            '%d artist has been classified as a graduate.',
            '%d artists have been classified as graduates.',
            updated,
        ) % updated, messages.SUCCESS)

    graduate.short_description = "Confirm graduated artists"

    def send_confirmation(self, request, queryset):
        from django.core.mail import send_mail
        for i in queryset:
            if i.user:
                send_mail('ZeroGravity Music Artist Application Approval',
                          f'Congratulations {i.name}! Your Artist application has been approved upon reviewal by our team.\n\nVisit your profile and the Artist section on our website to view your card.\nClick Artist Card for more information.\n\nZeroGravity Music Team',
                          'zgm@zerogravity.com.ng', [i.user], fail_silently=False)

                self.message_user(request, ngettext(
                    'Artist Confirmation Email has been sent to %d artist.',
                    'Artist Confirmation Email has been sent to %d artists.',
                    len(queryset),
                ) % len(queryset), messages.SUCCESS)

            else:
                self.message_user(request, "Artist does not have a registered email address ", level=messages.ERROR)

    send_confirmation.short_description = "Send Confirmation Email"

    def send_rejection(self, request, queryset):
        from django.core.mail import send_mail
        for i in queryset:
            if i.user:
                send_mail('ZeroGravity Music Artist Application Rejection',
                          f'Sorry {i.name}! Unfortunately, your Artist Application has not met up to all the requirements upon reviewal by our team.\n\nContact Us for more information about this on our website or social media accounts.\n\nZeroGravity Music Team',
                          'zgm@zerogravity.com.ng', [i.user], fail_silently=False)

                self.message_user(request, ngettext(
                    'Artist Rejection Email has been sent to %d artist.',
                    'Artist Rejection Email has been sent to %d artists.',
                    len(queryset),
                ) % len(queryset), messages.SUCCESS)

            else:
                self.message_user(request, "Artist does not have a registered email address ", messages.ERROR)

    send_rejection.short_description = "Send Rejection Email"




    list_display = ('name', 'university', 'status', 'verified', 'paid')
    list_filter = ('university', 'category', 'status', 'verified')
    search_fields = ['name', 'university__name']
    prepopulated_fields = {'slug': ('name',)}


class ArtistCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}




admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistCategory, ArtistCategoryAdmin)
