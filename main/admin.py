from django.contrib import admin
from .models import University, Advertisement, Video, Audio, CustomerService


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'active', 'type', 'posted')
    list_filter = ('type',)
    search_fields = ['title', 'owner','type']


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'feature', 'active', 'created')
    list_filter = ('active',)
    search_fields = ['title', 'feature']


class UniversityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CustomerServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ['name', 'email']


class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    list_filter = ['active']
    search_fields = ['title']



admin.site.register(University, UniversityAdmin)

admin.site.register(Advertisement, AdvertisementAdmin)

admin.site.register(Audio, AudioAdmin)

admin.site.register(Video, VideoAdmin)

admin.site.register(CustomerService, CustomerServiceAdmin)
