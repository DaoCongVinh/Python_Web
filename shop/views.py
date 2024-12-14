from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product,ContactForm,Cart,CartItem
from .forms import Contact_Form , RegisterForm , LoginForm
import json
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate,login
from django.contrib import messages

def homePage(request):
    return render(request, 'shop/homePage.html')

class loginView(View):
    def get(self, request):
        lF = LoginForm
        return render(request, 'shop/login.html', {'lF': lF})
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate (request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Đăng ký thành công!")
            return redirect('home')  
        else:
            messages.error(request, "Đăng nhập thất bại. Vui lòng kiểm tra thông tin.")
            return render(request, 'shop/login.html', {'lF': lF})
    
class register(View): #use class base view 
    def get(self, request):
        
        rF = RegisterForm() 
        return render(request, 'shop/register.html', {'rF': rF})

    def post(self, request):
        rF = RegisterForm(request.POST) 

        if rF.is_valid():
            username = rF.cleaned_data['username']
            email = rF.cleaned_data['email']
            password = rF.cleaned_data['password1']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Đăng ký thành công!")
            return redirect('login')  
        messages.error(request, "Đăng ký thất bại. Vui lòng kiểm tra thông tin.")
        return render(request, 'shop/register.html', {'rF': rF})

def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/product.html', context)

def product_list_home(request):
    hot_products = Product.objects.filter(status=Product.StatusChoices.HOT)
    new_products = Product.objects.filter(status=Product.StatusChoices.NEW)
    normal_products = Product.objects.filter(status=Product.StatusChoices.NORMAL)
    context = {
        'hot_products': hot_products,
        'new_products': new_products,
        'normal_products': normal_products
    }
    return render(request, 'shop/homePage.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.all().filter(brand=product.brand).exclude(id=product.id)
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/product_detail.html', context)


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
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart = Cart.objects.filter(session=session_key).first()
    context = {
        "cart": cart,
    }
    return render(request, "shop/cart.html", context)

@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        size = data.get("size")

        if not size:
            return JsonResponse({"success": False, "error": "Size is required"}, status=400)
        try:
            # Get the product
            product = get_object_or_404(Product, id=product_id)

            # Ensure the session exists
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            # Get or create the cart for the session
            cart, _ = Cart.objects.get_or_create(session=session_key)

            # Check if a CartItem with the same product and size exists
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=size, defaults={"quantity": 1}
            )

            if not created:
                # If the item exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()

            # Return a success response
            return JsonResponse({
                "success": True,
                "product_name": product.name,
                "size": size,
                "quantity": cart_item.quantity,
                "cart_total": cart.get_cart_total(),
                "cart_items_count": cart.get_cart_items_count()
            })
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"}, status=404)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

def delete_cart_item(request, item_id):
    if request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            cart = cart_item.cart
            cart_item.delete()
            cart_total = cart.get_cart_total()
            return JsonResponse({"success": True, "cart_total": cart_total})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})

def update_cart_item_quantity(request, item_id):
    if request.method == "POST":
        try:
            # Get the quantity from the request
            quantity = int(request.POST.get("quantity", 1))

            # Fetch the cart item
            cart_item = CartItem.objects.get(id=item_id)

            # Update the quantity
            cart_item.quantity = quantity
            cart_item.save()

            # Calculate the new total for this item
            item_total = cart_item.quantity * cart_item.product.price

            # Return a success response
            return JsonResponse({
                "success": True,
                "message": "Quantity updated successfully.",
                "item_total": item_total,  # Total for this item
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e),
            }, status=400)

    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    }, status=405)

@csrf_exempt
def get_cart_total(request):
    try:
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({"success": False, "message": "Cart not found."}, status=404)

        cart = Cart.objects.get(session=session_key)
        cart_total = cart.get_cart_total()
        return JsonResponse({"success": True, "cart_total": cart_total})
    except Cart.DoesNotExist:
        return JsonResponse({"success": False, "message": "Cart not found."}, status=404)
    
def product_search(request):
    query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    products_list = Product.objects.filter(
        Q(name__icontains=query) | Q(brand__icontains=query)
    ) if query else Product.objects.all()
    
    paginator = Paginator(products_list, 20)  # 20 products per page
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'shop/product.html', context)