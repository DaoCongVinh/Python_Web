# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('products/', views.product_list, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('saveContact/', views.saveContact, name='saveContact'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
]
