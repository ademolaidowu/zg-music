from django.shortcuts import render

from main.views import today, sat
from blog.models import Blog
from chart.models import Track
from main.models import Advertisement



def ZGMChartView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    tracks = Track.objects.filter(submission=1)
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')

    new = tracks.order_by('-released')[:10]
    zgmtop50 = tracks.filter(status=1).filter(zgm_rank__gte=1, zgm_rank__lte=50).order_by('zgm_rank')
    context = {
        'today': today(),
        'charted': sat(),
        'zgmtop50': zgmtop50,
        'new_tracks': new,
        'h_ads': h_ads,
        'blogs': blogs,
        'title': 'Chart - ZGM Top 50 | ZeroGravity',
    }
    return render(request, 'chart/zgm_chart.html', context)





