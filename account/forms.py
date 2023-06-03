from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


from .models import User, UserProfile, Subscriber
from artist.models import Artist
from chart.models import Track
from main.models import University



class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2'
        ]
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': ('Email')})
        self.fields['email'].label = False
        self.fields['username'].widget.attrs.update({'placeholder': ('Username')})
        self.fields['username'].label = False
        self.fields['password1'].widget.attrs.update({'placeholder': ('Password')})
        self.fields['password1'].label = False
        self.fields['password2'].widget.attrs.update({'placeholder': ('Repeat password')})
        self.fields['password2'].label = False





class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'})
        self.fields['password'].label = False





class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']





class SubscriptionForm(forms.ModelForm):
    subscriber_email = forms.EmailField(label='', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Your Email Address', 'rows': '1', 'cols': '50'}))

    class Meta:
        model = Subscriber
        fields = ['subscriber_email',]





class ArtistApplicationForm(forms.ModelForm):
    name = forms.CharField(label='Stage Name', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Fill in your stage name', 'rows': '1', 'cols': '50'}))

    university = forms.ModelChoiceField(queryset=University.objects.all(), label='University')

    ig_page = forms.CharField(label='Instagram', max_length=200)
    twitter_page = forms.CharField(label='Twitter', max_length=200, required=False)
    image = forms.ImageField(required=False)

    itunes = forms.CharField(label='Itunes Profile', max_length=200, required=False)
    audiomack = forms.CharField(label='Audiomack Profile', max_length=200, required=False)
    soundcloud = forms.CharField(label='Soundcloud Profile', max_length=200, required=False)

    class Meta:
        model = Artist

        help_texts = {
            'name': 'required',
            'university': 'required',
            'ig_page': 'required',
        }

        fields = [
            'name',
            'university',
            'ig_page',
            'twitter_page',
            'image',
            'itunes',
            'audiomack',
            'soundcloud',
        ]





class SongSubmissionForm(forms.ModelForm):
    title = forms.CharField(label='Track Title', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Fill in the Song Title', 'rows': '1', 'cols': '50'}))

    artist = forms.CharField(label='Artists', max_length=200)

    link = forms.CharField(label='Song Link', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter the link to the song', 'rows': '1', 'cols': '50'}))

    description = forms.CharField(required=False, label='Track Details', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Track Info, Please fill in your university here as well', 'rows': '4', 'cols': '50'}))

    artwork = forms.ImageField()

    released = forms.DateField(label='Release Date', help_text='Fill date in the format YYYY-MM-DD e.g 2019-12-25, 2018-06-08')


    class Meta:
        model = Track

        help_texts = {
            'title': 'required',
            'artist': 'required',
            'link': 'required',
        }

        fields = [
            'title',
            'artist',
            'link',
            'description',
            'artwork',
            'released',
        ]
