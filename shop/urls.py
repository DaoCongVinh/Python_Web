# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_home, name='home'),
    path('login/', views.login.as_view(), name='login'),
    path('register/', views.register.as_view(), name='register'),
    path('products/', views.product_list, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('saveContact/', views.saveContact, name='saveContact'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('update_quantity/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path("cart/total/", views.get_cart_total, name="cart_total"),
    path('search/', views.product_search, name='product_search'),
]
