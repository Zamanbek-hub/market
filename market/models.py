from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    name = models.CharField("category_name", max_length=100)
    image = models.ImageField(upload_to="category_image", blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"Category # {self.id} ({self.name})"


class Item(models.Model):
    image = models.ImageField(upload_to="item_image")
    name = models.CharField("item_name", max_length=255)
    description = models.CharField(max_length=500)
    added_date = models.DateTimeField("added_date", default=now)
    shelflife_date = models.DateField("shelflife_date", default=now)
    amount_in_stock = models.IntegerField(name="amount_in_stock", default=0)
    price = models.IntegerField(name="price", default=0)
    measure = models.CharField("measure", max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"Item # {self.id}"


class Delivery(models.Model):
    street = models.CharField("street", max_length=500, blank=True)
    building = models.CharField("building", max_length=500, blank=True)
    floor = models.CharField("floor", max_length=500, blank=True)
    apartment = models.CharField("apartment", max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Delivery # {self.street}"


class Payment(models.Model):
    payment = models.CharField("payment", max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment # {self.payment}"

    
class Basket(models.Model):
    token = models.CharField("token", max_length=100)

    def __str__(self):
        return f"Basket # {self.token}"
    

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)
    count = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)
    purchase_made = models.BooleanField(default=False)

    def __str__(self):
        return f"BasketItem # {self.item.name}"


