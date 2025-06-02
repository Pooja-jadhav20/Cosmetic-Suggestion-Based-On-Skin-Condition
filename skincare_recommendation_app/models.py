from django.db import models

# Create your models here.
class Function(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=120)
    ingridients = models.TextField()
    category = models.CharField(max_length=100)
    warning = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=150,blank=True, null=True)
    price = models.CharField(max_length=120,blank=True, null=True)
    review = models.CharField(max_length=150,blank=True, null=True)
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    function = models.CharField(max_length=50,blank=True, null=True)
    def __str__(self):
        return self.name
