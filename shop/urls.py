from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_list/', views.product_list, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('saveContact/',views.saveContact, name = 'saveContact'),
    path('login/',views.login, name="login"),
    path('register/',views.register, name="register"),
]
