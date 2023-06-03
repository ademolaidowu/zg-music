from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Author, Blog, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')
    list_filter = ('university',)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class BlogAdmin(admin.ModelAdmin):

    actions = ['make_published', 'make_withdrawn']
    def make_published(self, request, queryset):
        updated = queryset.update(status=1)
        self.message_user(request, ngettext(
            '%d blog post has been successfully published.',
            '%d blog posts have been successfully published.',
            updated,
        ) % updated, messages.SUCCESS)
    make_published.short_description = "Publish selected blogs"


    def make_withdrawn(self, request, queryset):
        updated = queryset.update(status=2)
        self.message_user(request, ngettext(
            '%d blog post has been successfully withdrawn.',
            '%d blog posts have been successfully withdrawn.',
            updated,
        ) % updated, messages.SUCCESS)
    make_withdrawn.short_description = "Withdraw selected blogs"


    list_display = ('title', 'author', 'status', 'created','updated')
    list_filter = ('status', 'author')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'posted')
    list_filter = ('post', 'name')
    search_fields = ['post__title', 'content']


admin.site.register(Author, AuthorAdmin)

admin.site.register(Blog, BlogAdmin)

admin.site.register(Comment, CommentAdmin)