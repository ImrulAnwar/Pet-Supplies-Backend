from django.db import models
from django.contrib.auth import get_user_model
from item_api.models import Item
import uuid

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_cost = models.PositiveBigIntegerField(default=70)
    item_count = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)

    def update_cart_totals(self):
        cart_items = self.items.all()
        self.item_count = cart_items.count()
        self.total_price = sum(
            item.sub_total_price for item in cart_items) + self.shipping_cost

    def save(self, *args, **kwargs):
        self.update_cart_totals()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cart for {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    sub_total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product_name} (Quantity: {self.quantity})"

    def save(self, *args, **kwargs):
        if self.item and self.quantity:
            self.sub_total_price = self.item.price * self.quantity
        super().save(*args, **kwargs)
        self.cart.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.save()
