from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Delivery)
admin.site.register(Payment)
admin.site.register(Basket)
admin.site.register(BasketItem)


