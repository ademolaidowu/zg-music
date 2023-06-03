from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path, include

from main.views import HomeView, LandingView, PlaylistView, VideoView, AboutView, ContactView
from blog.models import Blog
from main.views import today

blogs = Blog.objects.filter(status=1).order_by('-updated')

admin.site.site_header = "ZeroGravity Admin Panel"
admin.site.index_title = "ZGM Website Administration"
admin.site.site_title = "ZeroGravity"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('artists/', include('artist.urls')),
    path('blog/', include('blog.urls')),
    path('charts/', include('chart.urls')),


    path('', HomeView, name='home'),
    path('playlists/', PlaylistView, name='playlist-view'),
    path('zgmlink/', LandingView, name='landing-view'),
    path('videos/', VideoView, name='video-view'),
    path('about/', AboutView, name='about-view'),
    path('contact/', ContactView, name='contact-view'),


    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', extra_context={'blogs': blogs, 'today':today(), 'title': 'Account - Password Reset | ZeroGravity'}),
	 	name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html', extra_context={'blogs': blogs, 'today':today(), 'title': 'Account - Password Reset | ZeroGravity'}),
     	name='password_reset_done'),

	path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', extra_context={'blogs': blogs, 'today':today(), 'title': 'Account - Password Reset Confirm | ZeroGravity'}),
		name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html', extra_context={'blogs': blogs, 'today':today(), 'title': 'Account - Password Reset Confirm | ZeroGravity'}),
     	name='password_reset_complete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
