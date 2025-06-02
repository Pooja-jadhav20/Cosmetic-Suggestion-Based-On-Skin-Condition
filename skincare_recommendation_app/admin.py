from django.contrib import admin
from django_stisla.admin import site
from .models import Product
from .models import ProductType
from .models import Function

# Register your models here.
site.register(Product)
site.register(ProductType)
site.register(Function)