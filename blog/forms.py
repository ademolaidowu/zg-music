from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    name = forms.CharField(label='',
     widget=forms.Textarea(
        attrs={'class':'form-control', 'placeholder': 'Name', 'rows': '1', 'cols': '5'}))

    email = forms.EmailField(label='',
     widget=forms.Textarea(
        attrs={'class':'form-control', 'placeholder': 'E-mail', 'rows': '1', 'cols': '30'}))

    content = forms.CharField(label='',
     widget=forms.Textarea(
        attrs={'class':'form-control', 'placeholder': 'Comment here', 'rows': '4', 'cols': '60'}))

    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'content'
        ]

