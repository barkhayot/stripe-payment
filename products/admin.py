from django.contrib import admin
from .models import Product, Pack, Order

# Register your models here.


admin.site.register(Product)
admin.site.register(Pack)
admin.site.register(Order)