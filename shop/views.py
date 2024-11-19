from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,ContactForm
from .forms import Contact_Form


def home(request):
    return render(request, 'shop/home.html')

def shop(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'shop/shop.html', {'products': products})

def blog(request):
    blog_posts = [
        {
            "title": "The Cotton Jersey Zip-Up Hoodie",
            "content": "The Cotton Jersey Zip-Up Hoodie is a versatile and comfortable outerwear piece that combines style and functionality. Crafted from high-quality cotton jersey fabric, this hoodie offers a cozy feel and a casual yet fashionable look.",
            "image": "/img/blog/b1.jpg",
            "date": "13/01"
        },
        {
            "title": "How to Style a Quiff",
            "content": "The Quiff is a timeless and sophisticated hairstyle that never fails to make a statement. With its voluminous and sculpted front, it adds a touch of elegance and charm to any look.",
            "image": "img/blog/b2.jpg",
            "date": "13/04"
        },
                {
            "title": "The Cotton Jersey Zip-Up Hoodie",
            "content": "The Cotton Jersey Zip-Up Hoodie is a versatile and comfortable outerwear piece that combines style and functionality. Crafted from high-quality cotton jersey fabric, this hoodie offers a cozy feel and a casual yet fashionable look.",
            "image": "/img/blog/b1.jpg",
            "date": "13/01"
        },
        {
            "title": "How to Style a Quiff",
            "content": "The Quiff is a timeless and sophisticated hairstyle that never fails to make a statement. With its voluminous and sculpted front, it adds a touch of elegance and charm to any look.",
            "image": "img/blog/b2.jpg",
            "date": "13/04"
        },
        
        # Add more posts here
    ]
    return render(request, 'shop/blog.html', {'blog_posts': blog_posts})

def about(request):
    return render(request, 'shop/about.html')

# get input from forms to save as models 
def contact(request):
    cf = Contact_Form()
    return render(request, 'shop/contact.html' , {'cf':cf})

def saveContact(request):
    print("Request received at saveContact")  # Kiểm tra xem view có được gọi không
    if request.method == "POST":
        cf = Contact_Form(request.POST)
        if cf.is_valid():
            saveCF = ContactForm(
                username=cf.cleaned_data['username'],
                email=cf.cleaned_data['email'],
                subject=cf.cleaned_data['subject'],
                message=cf.cleaned_data['message']
            )
            saveCF.save()
            return HttpResponse("save success")
    else:
        return HttpResponse("not POST")
            

def cart(request):
    return render(request, 'shop/cart.html')

def product_detail(request, id):
    # Your logic to fetch product details using the id
    return render(request, 'shop/product.html', {'id': id})

def login(request):
    return render(request, 'shop/login.html')
def register(request):
    return render(request, 'shop/register.html')