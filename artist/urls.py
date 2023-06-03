from django.urls import path
from .views import (
    ArtistView,
    Polls,
)


app_name = 'artist'
urlpatterns = [
    path('', ArtistView, name='artist-view'),
    path('polls/', Polls, name='polls'),
]