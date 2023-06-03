from django.urls import path
from django.contrib.auth import views as auth_views

from .views import RegisterView, UserProfileView, ArtistApplicationView, SongSubmissionView
from .forms import AuthForm
from blog.models import Blog
from main.views import today

blogs = Blog.objects.filter(status=1).order_by('-updated')



app_name = 'account'
urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('profile/', UserProfileView, name='profile'),
    path('artist-application/', ArtistApplicationView, name='artistapplication-view'),
    path('song-submission/', SongSubmissionView, name='songsubmission-view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

 	path('login/', auth_views.LoginView.as_view(template_name='account/login.html',
                                                redirect_authenticated_user=True,
                                                authentication_form=AuthForm,
                                                extra_context={'blogs': blogs, 'today':today(), 'title': 'Account - Log In | ZeroGravity'}), name='login',),
]
