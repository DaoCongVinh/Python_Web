from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product,ContactForm,Cart,CartItem
from .forms import Contact_Form
import json


def homePage(request):
    return render(request, 'shop/homePage.html')

def login(request):
    return render(request, 'shop/login.html')
def register(request):
    return render(request, 'shop/register.html')

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
    return render(request, 'shop/product_detail.html', {'product': product})

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

        try:
            product = Product.objects.get(id=product_id)
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            cart, _ = Cart.objects.get_or_create(session=session_key)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({
                "success": True,
                "product_name": product.name,
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