from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from django.core.mail import send_mass_mail

from .models import Video, Advertisement
from artist.models import Artist
from blog.models import Blog
from chart.models import Track
from account.models import Subscriber
from .forms import CustomerServiceForm
from account.forms import SubscriptionForm



def sat():
    today_date = date.today()
    if today_date.strftime('%A') == 'Saturday':
        return today_date
    else:
        today = date.today().toordinal()
        lastWeek = today-7
        sunday = lastWeek - (lastWeek % 7)
        saturday = sunday + 6
        return date.fromordinal(saturday)



def today():
    today_date = datetime.now()
    return today_date




def LandingView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    context = {
        'today': today(),
        'blogs': blogs,
        'title': 'ZeroGravity - Music Charts, Blog, Playlist & Artists | ZeroGravity',
    }
    return render(request, "main/zgmlink.html", context)





def HomeView(request):
    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form = SubscriptionForm(request.POST or None)
        if subscription_form.is_valid():
            subscriber_email = request.POST.get('subscriber_email')
            subscriber = Subscriber.objects.create(email=subscriber_email)
            subscriber.save()

            message1 = ('ZeroGravity Music Team',
            'Thank you for subscribing to ZeroGravity.\nWe would keep you updated on the best musical content from ZeroGravity Music.',
            'zgm@zerogravity.com.ng',
            [subscriber_email])

            message2 = ('Newsletter Subscription Notification', f'This is to notify you that {subscriber_email} just subscribed to your newsletter',
                     'zgm@zerogravity.com.ng', ['zerogravityymusic@gmail.com'])

            send_mass_mail((message1, message2), fail_silently=True)

            messages.success(request, f'You have subscribed to ZeroGravity Music!')
            return redirect('home')
    else:
        subscription_form = SubscriptionForm()

    blogs = Blog.objects.filter(status=1)
    blog = blogs.order_by('-updated')
    popular = blogs.order_by('?')
    artists = Artist.objects.filter(status=1).order_by('?')[:6]
    tracks = Track.objects.filter(submission=1)
    recent = tracks.order_by('-released')[:10]
    artist_track = tracks.order_by('-released')
    zgmtop10 = tracks.filter(status=1).filter(zgm_rank__gte=1, zgm_rank__lte=10).order_by('zgm_rank')
    videos = Video.objects.filter(active=True)
    homevideos = videos.order_by('-created')[:5]
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')
    v_ads = ads.filter(type=2).order_by('?')
    video_ads = ads.filter(type=3).order_by('?')
    youtube_ads = ads.filter(type=4).order_by('?')
    common_tags = Blog.tags.most_common()[:5]

    context = {
        'today': today(),
        'charted': sat(),
    	'artists': artists,
        'tracks': artist_track,
        'blogs': blog,
        'popular_blogs': popular,
        'recent': recent,
        'zgmtop10': zgmtop10,
        'common_tags': common_tags,
        'videos': homevideos,
        'h_ads': h_ads,
        'v_ads': v_ads,
        'video_ads': video_ads,
        'youtube_ads': youtube_ads,
        'subscription_form': subscription_form,
        'title': 'ZeroGravity - Music Charts, Blog, Playlist & Artists | ZeroGravity',
    }
    return render(request, "main/home.html", context)





def PlaylistView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    context = {
        'today': today(),
        'blogs': blogs,
        'title': 'Playlists | ZeroGravity',
    }
    return render(request, "main/playlist.html", context)





def VideoView(request):
    videos = Video.objects.filter(active=True)
    videopage = videos.order_by('-created')
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    context = {
        'today': today(),
        'blogs': blogs,
        'videos': videopage,
        'title': 'Music Videos | ZeroGravity',
    }
    return render(request, "main/video.html", context)





def AboutView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    context = {
        'today': today(),
        'blogs': blogs,
        'title': 'About Us | ZeroGravity',
    }
    return render(request, "main/about.html", context)





def ContactView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    if request.method == 'POST':
        service_form = CustomerServiceForm(request.POST or None)
        if service_form.is_valid():
            customer_email = request.POST.get('email')
            request_content = request.POST.get('content')
            service_form.save()

            message1 = ('ZeroGravity Customer Support',
            'Thank you for contacting ZeroGravity Music.\nWe would get back to you shortly regarding your request.',
            'zgm@zerogravity.com.ng',
            [customer_email])

            message2 = ('Customer Service Request', f'You just got a request from {customer_email}.\n\nContent: {request_content}.\n\n Please attend to the customer as soon as possible.',
                     'zgm@zerogravity.com.ng', ['zerogravityymusic@gmail.com'])

            send_mass_mail((message1, message2), fail_silently=True)

            messages.success(request, f'Your message was sent successfully')
            return redirect('contact-view')
    else:
        service_form = CustomerServiceForm()

    context = {
        'today': today(),
        'blogs': blogs,
        'form': service_form,
        'title': 'Contact Us | ZeroGravity',
    }
    return render(request, "main/contact.html", context)


