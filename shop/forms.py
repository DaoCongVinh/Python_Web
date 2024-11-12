from django import forms
from .models import ContactForm

class Contact_Form(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['username', 'email', 'subject', 'message']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'cols': 30, 'rows': 10, 'class': 'form-control'}),
        }
