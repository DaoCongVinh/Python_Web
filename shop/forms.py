from django import forms
from .models import ContactForm

class Contact_Form(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['username', 'email', 'subject', 'message']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nhập tên của bạn', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Tiêu đề', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Lời nhắn', 'cols': 30, 'rows': 10, 'class': 'form-control'}),
        }

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30,required=True)
    email = forms.EmailField(max_length=30, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu và xác nhận mật khẩu không khớp.")

        return cleaned_data