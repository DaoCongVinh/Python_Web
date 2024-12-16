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
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    
class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100, label="Tên")
    phone = forms.CharField(max_length=15, label="Điện thoại liên lạc")
    address = forms.CharField(max_length=255, label="Địa chỉ")
    note = forms.CharField(widget=forms.Textarea, required=False, label="Ghi chú")
    payment = forms.ChoiceField(
        choices=[('COD', 'Thanh toán khi nhận hàng (COD)'), ('MoMo', 'Thanh toán bằng ví MoMo')],
        label="Phương thức thanh toán",
        widget=forms.RadioSelect
    )