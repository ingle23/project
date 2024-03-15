from django.contrib import admin
from .models import Customer,Grocery,Cart,Order
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','address','city','state','pincode']


@admin.register(Grocery)
class groceryAdmin(admin.ModelAdmin):
    list_display= ['id','name','category','storage_tips','nutrient_benefits','description','disclaimer','selling_price','discounted_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display= ['id','user','product','quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','grocery_product','quantity','order_at','status','total_price']