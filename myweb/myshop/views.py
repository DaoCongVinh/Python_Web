from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.db.models import Min, Max
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import intcomma

from myshop.models import Category, Brand, Product, Order, OrderDetail, Promotion
from myshop.templatetags.custom_filter import get_price_sale, get_price
# Create your views here.


def index(request): # View all product
    categories = Category.objects.filter(category_parent__isnull=True)
    products = Product.objects.all()
    minimum_price = products.aggregate(Min('price'))
    maximum_price = products.aggregate(Max('price'))
    products_promotion = Promotion.objects.filter(
            start_date__lte=now(),# ngày bắt dầu kmai < ngày hiện tại (trước ngày hiện tại)
            end_date__gt=now() # ngày kết thúc kmai > ngày hiện tại
            )
    return render(
        request=request,
        template_name='index.html',
        context={
            'categories': categories,
            'products': products,
            'minimum_price': minimum_price['price__min'],
            'maximum_price': maximum_price['price__max'],
            'products_promotion': products_promotion,
        }
    )


def brands(request, category_name): # View list product of a brand

    categories = Category.objects.filter(category_parent__isnull=True)
    brands = Category.objects.get(name=category_name).brand_set.all()
    brand_display = ''
    products = Product.objects.all()
    brand_search = request.GET.get('brand')
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    if brand_search:
        brand_display = Category.objects.get(name=category_name).brand_set.get(name=brand_search)
        products = products.filter(brand=brand_display)
    return render(
        request=request,
        template_name='common/brands.html',
        context={
            'brands': brands,
            'products': products,
            'category': category,
            'brand_display': brand_display,
            'categories': categories,
        }
    )


@login_required(login_url='/user/login')
def view_product(request, product_id): # View detail product when user click
    product_data = ''
    fields = []
    try:
        product_data = Product.objects.get(id=product_id)
        product_detail = product_data.detail
        fields_data = product_detail._meta.get_fields()
        for field in fields_data:
            if field.name == 'product' or field.name == 'id' or field.name == 'name':
                continue
            else:
                fields.append(field.name)
        info = f'Cấu hình chi tiết của {product_data}'
        return render(
        request=request,
        template_name='product/product-details.html',
        context={
            'info': info,
            'product_data': product_data,
            'fields': fields,
            'product_detail': product_detail,
        }             
        )
    except Product.DoesNotExist:
        return render(
            request=request,
            template_name='404.html',     
        )


@login_required(login_url='/user/login')
def add_product_to_cart(request, product_id): # Add a produc to user's cart
    try:
        # Xác định người dùng đăng nhập
        logged_user = request.user
        product_data = Product.objects.get(id=product_id)
        # Kiểm tra xem người dùng có giỏ hàng nào chưa thành công (Status = 0)
        user_has_ordered = Order.objects.get(user=logged_user, status=0) # Status = 0 là chưa thành công
        # Người dùng có 1 order chưa thành công.
        # Chia ra làm 2 trường hợp.
        
        # Người dùng thêm trùng với sản phẩm đã có trong giỏ hàng. Cập nhật dòng Orderdetail với sản phẩm đó và tăng quantity lên 1.
        order = user_has_ordered # Đổi tên lại cho dễ xử lý
        orderdetail = OrderDetail.objects.get(order=order, product=product_data)
        # orderdetail = order.orderdetail_set.get(product=product_data)
        # Qua dòng này thì đồng nghĩa sản phẩm thêm mới trùng với 1 trong các sản phẩm trong giỏ hàng.
        # Tăng quantity += 1
        if product_data.stock_quantity > orderdetail.quantity:
            orderdetail.quantity += 1
            orderdetail.amount = orderdetail.quantity * get_price(product_data.id)
            orderdetail.save()

    except Product.DoesNotExist: # Bỏ qua
        pass

    except Order.DoesNotExist:
        if product_data.stock_quantity >= 1:
            # Rơi vào except này thì người dùng không có đơn hàng chưa thành công. (Không có gì hoặc có đơn hàng thanh toán rồi Status = 1)
            # Tạo mới 1 order vói logged_user
            new_order = Order.objects.create(
                create_date=now(),
                total_amount=0,
                phone="",
                address="",
                status=0,
                user=logged_user,
            )
            # Order không có thông tin về sản phẩm nên tạo tiếp 1 Orderdetail
            OrderDetail.objects.create(
                product=product_data,
                order=new_order,
                quantity=1,
                amount=get_price(product_data.id),
            )

    except OrderDetail.DoesNotExist:
        if product_data.stock_quantity >= 1:
            # Người dùng thêm 1 sản phẩm không trùng với cái có trong giỏ hàng. Thêm mới 1 dòng Orderdetail với sản phẩm mới.
            OrderDetail.objects.create(
                product=product_data,
                order=order,
                quantity=1,
                amount=get_price(product_data.id)
            )
    user_ordered = Order.objects.get(user=logged_user, status=0)
    quantity = sum([item.quantity for item in user_ordered.orderdetail_set.all()])
    return JsonResponse(data={'quantity': quantity})


# 2 hàm view để tăng hoặc giảm
# def increase_quantity
# def decrease_quantity

# Viết 1 hàm hỗ trợ cả tăng hoặc giảm sản phẩm, 1 hàm có tới 2 tham số
@login_required(login_url='/user/login')
def change_product_quantity(request, action, product_id):
    # action: increase/decrease
    logged_user = request.user
    product_data = Product.objects.get(id=product_id)
    order = Order.objects.get(user=logged_user, status=0)
    orderdetail = OrderDetail.objects.get(order=order, product=product_data)
    if action == 'increase':
        if product_data.stock_quantity > orderdetail.quantity:
            orderdetail.quantity += 1
            orderdetail.amount = orderdetail.quantity * get_price(product_data.id)
            orderdetail.save()
    else:
        # decrease
        # Giảm tới quantity = 1, bấm thêm 1 lần nữa thì đồng nghĩa với xoá giỏ hàng
        if orderdetail.quantity == 1:
            orderdetail.delete()
        else:
            orderdetail.quantity -= 1
            orderdetail.amount = orderdetail.quantity * get_price(product_data.id)
            orderdetail.save()

    return redirect('show_cart')


@login_required(login_url='/user/login')
def delete_product_in_cart(request, product_id):
    logged_user = request.user   
    product_data = Product.objects.get(id=product_id)
    order = Order.objects.get(user=logged_user, status=0)
    orderdetail = OrderDetail.objects.get(order=order, product=product_data)
    orderdetail.delete()
    return redirect('show_cart')


@login_required(login_url='/user/login')
def show_cart(request):
    orderdetail=[]
    message=''
    total_amount=0
    try:
        logged_user = request.user
        order = Order.objects.get(user=logged_user, status=0)
        orderdetail = order.orderdetail_set.all()
        if len(orderdetail) == 0:
            message = 'Chưa có sản phẩm trong giỏ hàng'
        else:
            total_amount = sum([item.amount for item in orderdetail])
    except:
        message = 'Chưa có sản phẩm trong giỏ hàng'
    
    return render(
        request=request,
        template_name='cart/cart.html',
        context={
            'data_orderdetail': orderdetail,
            'message': message,
            'total_amount': total_amount,
        }
    )

@login_required(login_url='/user/login')
def checkout(request):
    orderdetail=[]
    logged_user = request.user
    order = Order.objects.get(user=logged_user, status=0)
    orderdetail = order.orderdetail_set.all()
    if request.method == "POST":
        phone=request.POST['phone']
        address=request.POST['address']
        order.phone = phone
        order.address = address
        order.total_amount = sum([item.amount for item in orderdetail])
        order.status = 1 # Đơn hàng thành công
        order.save()
        for od_detail in orderdetail:
            od_detail.product.stock_quantity -= od_detail.quantity
            od_detail.product.save()
        # embed send mail
        # html_template = 'cart/message.html'
        # context={
        #     'data_orderdetail': orderdetail,
        #     'total_amount': order.total_amount,
        # }
        # html_template = render_to_string(html_template, {'context':context})

        from_email = settings.EMAIL_HOST_USER
        subject = 'Thanks for your checkout at shop Django'
        message = f'''
        Hi {logged_user.username},
        Thanks for your check out.
        Total amount: {intcomma(order.total_amount)} VND

        Thanks
        Shop django
        '''
        recipient_list = [logged_user.email]
        send_mail(subject, message, from_email, recipient_list)
        
        return redirect('index')

    return render(
        request=request,
        template_name='cart/checkout.html',
        context={
            'data_orderdetail': orderdetail,
            'total_amount': order.total_amount,
        }
    )

