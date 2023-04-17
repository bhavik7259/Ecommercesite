from django.db import models
from django.conf import settings

User=settings.AUTH_USER_MODEL

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=500)
    image=models.ImageField(upload_to="static/images",default="")

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()


    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.objects.all()

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity=models.IntegerField()
    status = models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Orderitem(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=250)
    pro_id = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id.username
