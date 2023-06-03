from django import forms
from .models import CustomerService

class CustomerServiceForm(forms.ModelForm):
    class Meta:
        model = CustomerService
        fields = [
            'name',
            'email',
            'phone',
            'content',
        ]


    def __init__(self, *args, **kwargs):
        super(CustomerServiceForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
        self.fields['name'].label = False
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['email'].label = False
        self.fields['phone'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Phone Number(Optional)'})
        self.fields['phone'].label = False
        self.fields['content'].widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'How can we help you?'})
        self.fields['content'].label = False
        self.fields['content'].widget.attrs['rows'] = 10

