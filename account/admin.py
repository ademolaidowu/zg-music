from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile, Subscriber


class UserAdmin(BaseUserAdmin):
	fieldsets = (
	    (None, {'fields': ('email', 'username', 'password', 'first_name', 'last_name', 'last_login')}),
	    ('Permissions', {'fields': (
	        'is_active',
	        'is_staff',
	        'is_admin',
	        'is_superuser',
	        'groups',
	        'user_permissions',
	    )}),
	)
	add_fieldsets = (
	    (
	        None,
	        {
	            'classes': ('wide',),
	            'fields': ('email', 'username', 'password1', 'password2')
	        }
	    ),
	)

	list_display = ('email', 'username', 'is_staff', 'last_login')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ('groups', 'user_permissions',)



class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'is_artist', 'artist_user')
	list_filter = ('is_artist',)
	search_fields = ['user', 'artist_user__name']



class SubscriberAdmin(admin.ModelAdmin):
	list_display = ('email', 'date_joined')
	search_fields = ['email',]



admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
