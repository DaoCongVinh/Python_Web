from django import forms
from django.core.exceptions import ValidationError # Import module văng lỗi
from django.contrib.auth.models import User
from .models import Pet # import Form
# ModelForm: Form được tạo từ Model -> tạo ra những ô input y như định nghĩa của model.
# Form: Dạng Freestyle/custom form.

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet # Tạo Form cho Model nào
        fields = '__all__' #('name', 'age', 'type') # Chọn ô input cho cột nào trong Table được hiển thị
        widgets = { # Thêm các thuộc tính HTML vào các ô input của Form
            'id': forms.TextInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'age': forms.NumberInput(attrs={'class':'form-control'}),
            'type': forms.Select(attrs={'class':'form-control'}),
            'weight': forms.NumberInput(attrs={'class':'form-control'}),
            'length': forms.NumberInput(attrs={'class':'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class':'form-control'}),
            'vacinated': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'dewormed': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'sterilized': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        } # Dùng để định nghĩa trường thông tin, attrs là thuộc tính của TextInput

# Khi tạo server validate thì tạo ở phí forms.
# Khi muốn validate cho 1 field thì tạo hàm có dạng clean_<tên field muốn validate>
# Pet không được trùng tên, id
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            print(self.instance)
            self.fields.pop('id', None)
            # self.fields["id"].disabled = True
            # self.fields["id"].widget.attrs["readonly"] = True

    def clean_id(self):
        # print("Validate Id")
        # Thử lấy Pet với id người dùng gửi lên
        # Nếu trả về 1 pet object thì Id đã trùng báo lỗi
        # Nếu mà không trả về thì Id chưa trùng, trả lại Id tiếp tục xử lý

        try:
            pet_id = self.cleaned_data['id']
            Pet.objects.get(id=pet_id)
            # print('Id đã trùng, văng lỗi')
            raise ValidationError(f'Pet với ID={pet_id} đã tồn tại, vui lòng nhập ID khác')

        except Pet.DoesNotExist:
            print('Pet với Id chưa tồn tại')
            return self.cleaned_data['id']


    def clean_name(self):
        if self.instance.id and self.instance.name == self.cleaned_data['name']:
            return self.cleaned_data['name']
        try:
            pet_name = self.cleaned_data['name']
            Pet.objects.get(name=pet_name)
            raise ValidationError(f'Pet với name={pet_name} đã tồn tại, vui lòng nhập Id khác')

        except Pet.DoesNotExist:
            print('Pet với name chưa tồn tại')
            return self.cleaned_data['name']

# Form đăng ký RegistrationForm
# Bắt buộc người dùng phải điền:
    # Username: không được trùng
    # Password: 
    # Firstname
    # Lastname
    # Email: không được trùng
class RegistrationForm(forms.Form):
    username = forms.CharField(
        label="Tên Đăng Nhập",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        label="Mật Khẩu",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    confirm_password = forms.CharField(
        label="Nhập Lại Mật Khẩu",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    first_name = forms.CharField(
        label="Tên",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    last_name = forms.CharField(
        label="Họ",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    email = forms.EmailField(
        label="Email",
        max_length=20,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
        )

    # Kiểm tra username, email không bị trùng và password và confirm_password phải giống nhau
    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise ValidationError(f'Tên đăng nhập đã trùng')

        except User.DoesNotExist:
            return username

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise ValidationError(f'Email đã trùng')

        except User.DoesNotExist:
            return email

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError('Mật khẩu và nhập lại mật khẩu không trùng nhau')
        return self.cleaned_data['confirm_password']

    def save(self):
        User.objects.create_user(# create_user là lưu vào CSDL có hass password. create là lưu dạng raw_data
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Tên Đăng Nhập",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        label="Mật Khẩu",
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

    # Hàm kiểm tra thông tin người dùng gửi lên
    # Lấy username, password check thông tin
    # def clean_password(self):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #     try:
    #         # Thử get User từ username và password
    #         # 