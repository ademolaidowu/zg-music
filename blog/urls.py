from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    AuthorDetailView,
    ArchiveListView,
    TagBlogListView
)


app_name = 'blog'
urlpatterns = [
    path('', BlogListView, name='blog-list'),
    path('<slug:slug>/', BlogDetailView, name='blog-detail'),
    path('author/<slug:slug>/', AuthorDetailView, name='author-detail'),
    path('archives/<int:year>/<int:month>/', ArchiveListView, name='archive-list'),
    path('tag/<slug:slug>/', TagBlogListView, name='tagblog-list'),
]