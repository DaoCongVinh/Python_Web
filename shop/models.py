# models.py
from django.db import models

class Product(models.Model):
    class StatusChoices(models.TextChoices):
        HOT = 'Hot', 'Hot'
        NEW = 'New', 'New'
        NORMAL = 'Normal', 'Normal'
        
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    image_url = models.URLField()  # Adjust based on how you store images
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField()  # Adjust based on how you store ratings
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.NORMAL,  # Default status
    )

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Represents a shopping cart linked to a session."""
    session = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.session}"

    def get_cart_total(self):
        """Calculate the total price of items in the cart."""
        return sum(item.get_total_price() for item in self.items.all())

    def get_cart_items_count(self):
        """Calculate the total number of items in the cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Represents a single product in the cart."""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """Calculate the total price for this cart item."""
        return self.quantity * self.product.price
    
class ContactForm(models.Model):
    username = models.CharField(max_length = 25)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.username
    

    