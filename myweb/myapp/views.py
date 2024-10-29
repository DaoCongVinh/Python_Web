from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from myapp.models import Pet
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from myapp.forms import PetForm # Import PetForm Class

# Create your views here.
# View đầu tiên
# File views.py đóng vai trò là chữ C trong MVC.
# R: READ
def index(request):
    pets = Pet.objects.all()
    search = request.GET.get('search')
    if search:
        pets = Pet.objects.filter(name__icontains=search)
    paginator = Paginator(object_list=pets, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    message = "Không có Pet" if len(pets) == 0 else ""
        
    return render(
        request=request,
        template_name='pet/index.html',
        context={
            'pets': pets,
            'message': message,
            'page_obj': page_obj,
        }
    )

# C: CREATE
# Người dùng phải đăng nhập thì mới add được pet
@login_required(login_url='/user/login')
def add_pet(request):
    form = PetForm() # Khởi tạo Form
    if request.method == "POST":
        # Validation form: kiểm tra tính hợp lệ dữ liệu đầu vào trên browser
        # Server validation
        form = PetForm(request.POST)
        if form.is_valid(): # Server validate có sẵn
            # print("Validate ok")
            form.save() # Giống Model save()
            return redirect('index')
        # else:
        #     print('Lỗi')
        # Pet.objects.create(
        #     id=request.POST['pet_id'],
        #     name=request.POST['pet_name'],
        #     age=request.POST['pet_age'],
        #     type=request.POST['pet_type'],
        #     weight=request.POST['pet_weight'],
        #     length=request.POST['pet_length'],
        #     color=request.POST['pet_color'],
        #     vacinated=request.POST.get('pet_vacinated', 'off') == 'on',
        #     dewormed=request.POST.get('pet_dewormed', 'off') == 'on',
        #     sterilized=request.POST.get('pet_sterilized', 'off') == 'on',
        # )
    return render(
        request=request,
        template_name='pet/add.html',
        context={
            'form': form
        } # Truyền Form

    )

# U: UPDATE
@login_required(login_url='/user/login')
def update_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    form = PetForm(instance=pet)
    if request.method == "POST":
        form = PetForm(request.POST, instance=pet)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        # else:
        #     print(form.errors)
        # pet.name=request.POST['pet_name']
        # pet.age=request.POST['pet_age']
        # pet.type=request.POST['pet_type']
        # pet.weight=request.POST['pet_weight']
        # pet.length=request.POST['pet_length']
        # pet.color=request.POST['pet_color']
        # pet.vacinated=request.POST.get('pet_vacinated', 'off') == 'on'
        # pet.dewormed=request.POST.get('pet_dewormed', 'off') == 'on'
        # pet.sterilized=request.POST.get('pet_sterilized', 'off') == 'on'
        # pet.save()
    return render(
        request=request,
        template_name='pet/update.html',
        context={
            'form': form
        }
    )

# V: VIEWS
@login_required(login_url='/user/login')
def detail_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    form = PetForm(instance=pet)
    return render(
        request=request,
        template_name='pet/detail.html',
        context={
            'form': form
        }
    )


# D: DELETE
@login_required(login_url='/user/login')
def delete_pet(request,pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet.delete()
    return redirect('index')


# def students(request):
#     students = Student.objects.all()
#     # response = HttpResponse()
#     # response.write("<h1>Danh sách các student trong Database</h1>")
#     # response.write("<ol>")
#     # for student in students:
#     #     response.write(f"<li>Name: {student.name}, Age: {student.age} </li>")
#     # response.write("</ol>")
#     # return response
#     return render(
#         request=request,
#         template_name='students.html',
#         context={
#             'students': students # key <tên biến sẽ dùng HTML>: value <value là giá trị biến bên trong python truyền vào>
#         }# Biến được truyền từ Views sang Template HTML
#     )

# def add_student(request):
#     if request.method == "POST":
#         # print(request.POST) # In kết quả trả về máy chủ
#         Student.objects.create(
#             name=request.POST['name'],
#             age=int(request.POST['age']),
#             gender=request.POST['gender']=="True",
#             email=request.POST['email'],
#             phone=request.POST['phone'],
#             address=request.POST['address']
#         )
#         return redirect('students')
#         # # return HttpResponseRedirect('myapp/students')
#     return render(
#         request=request,
#         template_name='add_student.html'
#     )

# # 2 cách
# # Function base view - class base view
# def my_view(request): # Hàm trong views.py sẽ luôn có 1 tham số phải có
#     # request: HTTP request
#     # response = HttpResponse()
#     # response.write("<h1>Hello các bạn lớp PYTHON2204</h1>")
#     # response.write("<p style='color:Blue;'>Hello các bạn lớp PYTHON2204</p>")
#     # Phải trả về là HTTP response
#     if request.method == "POST":
#         request.session['username'] = request.POST['name-username']
#     return render(request,'myview.html')


# #Thứ tự dùng để tạo 1 view mới trong Django
# #B1: Tạo hàm trong view.py
# def welcome(request):
    # response = HttpResponse()
    # response.write(f"Welcome {request.session['username']}")
    # return response
