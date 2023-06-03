from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .models import Blog, Comment
from .forms import CommentForm
from main.views import today
from main.models import Advertisement
from account.models import Subscriber
from account.forms import SubscriptionForm



def BlogListView(request):
    blog = Blog.objects.filter(status=1)
    blogs = blog.order_by('-updated')
    popular = blog.order_by('?')
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')
    v_ads = ads.filter(type=2).order_by('?')
    video_ads = ads.filter(type=3).order_by('?')
    youtube_ads = ads.filter(type=4).order_by('?')
    common_tags = Blog.tags.most_common()[:5]

    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = blogs.filter(title__icontains=search_term)
    else:
        posts = blogs

        paginator = Paginator(posts, 8)
        page = request.GET.get('page')
        posts = paginator.get_page(page)


    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form = SubscriptionForm(request.POST or None)
        if subscription_form.is_valid():
            subscriber_email = request.POST.get('subscriber_email')
            subscriber = Subscriber.objects.create(email=subscriber_email)
            subscriber.save()
            send_mail(
                'ZeroGravity',
                'Thank you for subscribing to ZeroGravity.\nWe would keep you updated on the best musical content from ZeroGravity Music.',
                'zgm@zerogravity.com.ng',
                [subscriber_email],
                fail_silently=True,
            )
            messages.success(request, f'You have subscribed to ZeroGravity Music!')
            return redirect('blog:blog-list')
    else:
        subscription_form = SubscriptionForm()


    context = {
        'today': today(),
        'posts': posts,
        'blogs': blogs,
        'popular_blogs': popular,
        'common_tags': common_tags,
        'h_ads': h_ads,
        'v_ads': v_ads,
        'video_ads': video_ads,
        'youtube_ads': youtube_ads,
        'subscription_form': subscription_form,
        'title': 'Blog | ZeroGravity',
    }
    return render(request, "blog/blog_list.html", context)



def BlogDetailView(request, slug):
    blog = Blog.objects.filter(status=1)
    blogs = blog.order_by('-updated')
    popular = blog.order_by('?')
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')
    v_ads = ads.filter(type=2).order_by('?')
    video_ads = ads.filter(type=3).order_by('?')
    youtube_ads = ads.filter(type=4).order_by('?')
    common_tags = Blog.tags.most_common()[:5]

    post_obj = blogs.get(slug=slug)
    comment_obj = Comment.objects.filter(active=True).filter(post=post_obj, reply=None)

    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form = SubscriptionForm(request.POST or None)
        if subscription_form.is_valid():
            subscriber_email = request.POST.get('subscriber_email')
            subscriber = Subscriber.objects.create(email=subscriber_email)
            subscriber.save()
            send_mail(
                'ZeroGravity',
                'Thank you for subscribing to ZeroGravity.\nWe would keep you updated on the best musical content from ZeroGravity Music.',
                'zgm@zerogravity.com.ng',
                [subscriber_email],
                fail_silently=True,
            )
            messages.success(request, f'You have subscribed to ZeroGravity Music!')
            return redirect(post_obj.get_absolute_url())
    else:
        subscription_form = SubscriptionForm()


    if request.method == 'POST' and 'subscribe' not in request.POST:
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post_obj, name=name, email=email, content=content, reply=comment_qs)
            comment.save()
            return redirect(post_obj.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'today': today(),
        'blogs': blogs,
        'popular_blogs': popular,
        'posts': post_obj,
        'common_tags': common_tags,
        'h_ads': h_ads,
        'v_ads': v_ads,
        'video_ads': video_ads,
        'youtube_ads': youtube_ads,
        'subscription_form': subscription_form,
        'comments': comment_obj,
        'comment_form': comment_form,
        'title': post_obj.title + ' | ZeroGravity',
	}
    return render(request, 'blog/blog_detail.html', context)



def AuthorDetailView(request, slug):
    blog = Blog.objects.filter(status=1)
    blogs = blog.order_by('-updated')
    popular = blog.order_by('?')
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')
    v_ads = ads.filter(type=2).order_by('?')
    video_ads = ads.filter(type=3).order_by('?')
    youtube_ads = ads.filter(type=4).order_by('?')
    common_tags = Blog.tags.most_common()[:5]

    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = blogs.filter(title__icontains=search_term)
    else:
        posts = blogs.filter(author__slug=slug)

        paginator = Paginator(posts, 8)
        page = request.GET.get('page')
        posts = paginator.get_page(page)


    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form = SubscriptionForm(request.POST or None)
        if subscription_form.is_valid():
            subscriber_email = request.POST.get('subscriber_email')
            subscriber = Subscriber.objects.create(email=subscriber_email)
            subscriber.save()
            send_mail(
                'ZeroGravity',
                'Thank you for subscribing to ZeroGravity.\nWe would keep you updated on the best musical content from ZeroGravity Music.',
                'zgm@zerogravity.com.ng',
                [subscriber_email],
                fail_silently=True,
            )
            messages.success(request, f'You have subscribed to ZeroGravity Music!')
            return redirect('blog:author-detail', slug)
    else:
        subscription_form = SubscriptionForm()


    context = {
        'today': today(),
        'posts': posts,
        'blogs': blogs,
        'popular_blogs': popular,
        'common_tags': common_tags,
        'h_ads': h_ads,
        'v_ads': v_ads,
        'video_ads': video_ads,
        'youtube_ads': youtube_ads,
        'subscription_form': subscription_form,
        'title': 'Blog Author | ZeroGravity',
    }
    return render(request, "blog/author_detail.html", context)



def TagBlogListView(request, slug):
    blog = Blog.objects.filter(status=1)
    blogs = blog.order_by('-updated')
    popular = blog.order_by('?')
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')
    v_ads = ads.filter(type=2).order_by('?')
    video_ads = ads.filter(type=3).order_by('?')
    youtube_ads = ads.filter(type=4).order_by('?')
    common_tags = Blog.tags.most_common()[:5]

    tag = Blog.tags.filter(slug=slug).first()

    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = blogs.filter(title__icontains=search_term)
    else:
        posts = blogs.filter(tags__slug=slug)


        paginator = Paginator(posts, 8)
        page = request.GET.get('page')
        posts = paginator.get_page(page)


    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form = SubscriptionForm(request.POST or None)
        if subscription_form.is_valid():
            subscriber_email = request.POST.get('subscriber_email')
            subscriber = Subscriber.objects.create(email=subscriber_email)
            subscriber.save()
            send_mail(
                'ZeroGravity',
                'Thank you for subscribing to ZeroGravity.\nWe would keep you updated on the best musical content from ZeroGravity Music.',
                'zgm@zerogravity.com.ng',
                [subscriber_email],
                fail_silently=True,
            )
            messages.success(request, f'You have subscribed to ZeroGravity Music!')
            return redirect('blog:tagblog-list', slug)
    else:
        subscription_form = SubscriptionForm()


    context = {
        'today': today(),
        'posts': posts,
        'blogs': blogs,
        'popular_blogs': popular,
        'tag_title': tag,
        'common_tags': common_tags,
        'h_ads': h_ads,
        'v_ads': v_ads,
        'video_ads': video_ads,
        'youtube_ads': youtube_ads,
        'subscription_form': subscription_form,
        'title': 'Blog | ZeroGravity',
    }
    return render(request, "blog/tagblog_list.html", context)



def ArchiveListView(request, year, month):
    blog = Blog.objects.filter(status=1)
    blogs = blog.order_by('-updated')
    popular = blog.order_by('?')
    ads = Advertisement.objects.filter(active=True)
    h_ads = ads.filter(type=1).order_by('?')
    v_ads = ads.filter(type=2).order_by('?')
    video_ads = ads.filter(type=3).order_by('?')
    youtube_ads = ads.filter(type=4).order_by('?')
    common_tags = Blog.tags.most_common()[:5]

    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = blogs.filter(title__icontains=search_term)
    else:
        posts = blogs.filter(updated__year=year).filter(updated__month=month)

        paginator = Paginator(posts, 8)
        page = request.GET.get('page')
        posts = paginator.get_page(page)


    if request.method == 'POST' and 'subscribe' in request.POST:
        subscription_form = SubscriptionForm(request.POST or None)
        if subscription_form.is_valid():
            subscriber_email = request.POST.get('subscriber_email')
            subscriber = Subscriber.objects.create(email=subscriber_email)
            subscriber.save()
            send_mail(
                'ZeroGravity',
                'Thank you for subscribing to ZeroGravity.\nWe would keep you updated on the best musical content from ZeroGravity Music.',
                'zgm@zerogravity.com.ng',
                [subscriber_email],
                fail_silently=True,
            )
            messages.success(request, f'You have subscribed to ZeroGravity Music!')
            return redirect('blog:archive-list', year, month)
    else:
        subscription_form = SubscriptionForm()


    context = {
        'today': today(),
        'posts': posts,
        'blogs': blogs,
        'popular_blogs': popular,
        'common_tags': common_tags,
        'h_ads': h_ads,
        'v_ads': v_ads,
        'video_ads': video_ads,
        'youtube_ads': youtube_ads,
        'subscription_form': subscription_form,
        'title': 'Blog Archive | ZeroGravity',
    }
    return render(request, "blog/archive_list.html", context)


