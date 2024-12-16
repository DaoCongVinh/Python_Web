# models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    class StatusChoices(models.TextChoices):
        HOT = 'Hot', 'Hot'
        NEW = 'New', 'New'
        NORMAL = 'Normal', 'Normal'
        
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    image_url = models.URLField() 
    price = models.DecimalField(max_digits=10, decimal_places=0)

    @property
    def formatted_price(self):
        return f"{self.price:,.0f}"
    rating = models.IntegerField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.NORMAL,  # Default status
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Represents a shopping cart linked to a session."""
    session = models.CharField(max_length=255, unique=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.session}"

    def get_cart_total(self):
        """Calculate the total price of items in the cart."""
        return sum(item.get_total_price() for item in self.items.all())
    
    def formatted_total_price(self):
        return f"{self.get_cart_total():,.0f}"

    def get_cart_items_count(self):
        """Calculate the total number of items in the cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Từng sản phẩm trong giỏ hàng"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product', 'size')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """Calculate the total price for this cart item."""
        return self.quantity * self.product.price
    
    def formatted_total_price(self):
        return f"{self.get_total_price():,.0f}"
    
    def get_cart_total(self):
        return sum(item.get_total_price() for item in self.items.all())
    
class ContactForm(models.Model):
    username = models.CharField(max_length = 25)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.username
    
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Thanh toán khi nhận hàng (COD)'),
        ('MoMo', 'Thanh toán bằng ví MoMo'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # Link to the user
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    note = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username} - {self.payment_method}"
    
class OrderItem(models.Model):
    """Represents an individual item in an order."""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
