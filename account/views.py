from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail


from .forms import RegistrationForm, ArtistApplicationForm, SongSubmissionForm, UserUpdateForm, ProfileUpdateForm
from main.views import today
from blog.models import Blog
from chart.models import Track



def RegisterView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created!')
            return redirect('account:login')
    else:
        form = RegistrationForm()
    context = {
        'today': today(),
        'form': form,
        'blogs': blogs,
        'title': 'Account - Sign Up | ZeroGravity',
    }
    return render(request,'account/register.html', context)





@login_required
def UserProfileView(request):
    artist_track = Track.objects.filter(submission=1).order_by('-released')
    blogs = Blog.objects.filter(status=1).order_by('-updated')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile Information has been updated!')
            return redirect('account:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()

    context = {
        'today': today(),
        'u_form': u_form,
        'p_form': p_form,
        'blogs': blogs,
        'tracks': artist_track,
        'title': 'Account - Profile | ZeroGravity',
    }
    return render(request, 'account/profile.html', context)





@login_required
def ArtistApplicationView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')

    if request.method == 'POST':
            application_form = ArtistApplicationForm(request.POST, request.FILES)
            if application_form.is_valid():
                obj = application_form.save(commit=False)
                obj.user = request.user
                obj.save()

                message1 = ('ZeroGravity Music Team',
                'Your Artist Application has been submitted and is under review.\nWe would get back to you soon.',
                'zgm@zerogravity.com.ng',
                [request.user])

                message2 = ('Artist Confirmation Request', f'This is to notify you that {request.user} just applied to be an artist on your platform.\nKindly review his application and get back to him.',
                         'zgm@zerogravity.com.ng', ['zerogravityymusic@gmail.com'])

                send_mass_mail((message1, message2), fail_silently=True)

                messages.success(request, f'Your Application was successful!')
                return redirect('account:profile')
            else:
                messages.error(request, f'Your Form is invalid!')
    else:
        application_form = ArtistApplicationForm

    context = {
        'today': today(),
        'blogs': blogs,
        'form': application_form,
        'title': ' Account - Artist Application | ZeroGravity',
    }
    return render(request, 'account/artist_application.html', context)





@login_required
def SongSubmissionView(request):
    blogs = Blog.objects.filter(status=1).order_by('-updated')

    if request.method == 'POST':
            submission_form = SongSubmissionForm(request.POST, request.FILES)
            if submission_form.is_valid():
                song_title = request.POST.get('title')
                obj = submission_form.save(commit=False)
                obj.user = request.user
                obj.save()

                message1 = ('ZeroGravity Music Team',
                f'Your Song {song_title} has been submitted to ZeroGravity Music Team and is now under review.',
                'zgm@zerogravity.com.ng',
                [request.user])

                message2 = ('Song Review Request', f'This is to notify you that the track {song_title} was submitted by {request.user} to be placed under review for charting and playlisting.\nKindly review the track and take necessary actions.',
                         'zgm@zerogravity.com.ng', ['zerogravityymusic@gmail.com'])

                send_mass_mail((message1, message2), fail_silently=True)

                messages.success(request, f'Your Song {song_title} was submitted succesfully!')
                return redirect('account:profile')
            else:
                messages.error(request, f'Your Form is invalid!')
    else:
        submission_form = SongSubmissionForm()

    context = {
        'today': today(),
        'blogs': blogs,
        'form': submission_form,
        'title': ' Account - Song Submission | ZeroGravity',
    }
    return render(request, 'account/song_submission.html', context)

