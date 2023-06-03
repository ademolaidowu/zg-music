from django.shortcuts import render
from django.core.paginator import Paginator


from main.views import today
from .models import Artist
from blog.models import Blog
from main.models import Advertisement
from chart.models import Track

from django.http import HttpResponse

def ArtistView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    artists = Artist.objects.filter(status=1).order_by('name')
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')
    artist_track = Track.objects.filter(submission=1).order_by('-released')

    if 'search' in request.GET:
        search_term = request.GET['search']
        artist = artists.filter(name__icontains=search_term)

    else:
        artist = artists

        paginator = Paginator(artist, 12)
        page = request.GET.get('page')
        artist = paginator.get_page(page)

    context = {
        'today': today(),
        'h_ads': h_ads,
        'blogs': blogs,
        'tracks': artist_track,
        'artist': artist,
        'title': ' Artists | ZeroGravity',
    }
    return render(request, "artist/artist_list.html", context)



def Polls(request):
    return HttpResponse("Hello, world. 445d9b9c is the polls index.")
