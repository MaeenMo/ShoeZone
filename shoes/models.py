from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


class Shoe(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=20, default="Nike")
    price = models.CharField(max_length=10, default="EGP 50")
    size = models.CharField(max_length=50, default="38 - 45")
    color = models.CharField(max_length=50, default="White")
    color_hexa = models.CharField(max_length=50, default="#000000")
    Type = models.CharField(max_length=10, default="Men")
    img = models.ImageField(upload_to='shoes_images')
    shoe_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Cart_item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    selected_size = models.CharField(max_length=80, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    order_num = models.CharField(max_length=20, default="#000000")

    def __str__(self):
        return "In Cart: {x} ({y})".format(x=self.product.name, y=self.owner)


class Order(models.Model):
    user_ordered = models.CharField(max_length=50, default="")
    order_no = models.CharField(max_length=20, default="#000000")
    items = models.TextField(max_length=1000, default="")
    total_price = models.CharField(max_length=20, default="")

    def __str__(self):
        return str(self.order_no)
