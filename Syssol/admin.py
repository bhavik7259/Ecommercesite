from django.contrib import admin

# Register your models here.
from .models import Product,Category,Cart,Orderitem

class AdminCart(admin.ModelAdmin):
    list_display=['user','product','quantity']

class AdminOrderitem(admin.ModelAdmin):
    list_display=['user_id','pro_id','status']

class AdminProduct(admin.ModelAdmin):
    list_display=['product_name','category','price']


admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Cart,AdminCart)
admin.site.register(Orderitem,AdminOrderitem)
