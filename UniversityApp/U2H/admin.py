from django.contrib import admin
from .models import FoodItems, Users, Categorie, Order, Cleanliness

# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display=['id','item_name','price','category']

class CategoryProduct(admin.ModelAdmin):
    list_display=['category_name']

class UserAccounts(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'prn', 'password']

class OrderedItems(admin.ModelAdmin):
    list_display=['food_item', 'user', 'quantity', 'total_price', 'date']

class CleanlinessData(admin.ModelAdmin):
    list_display=['user', 'building_name', 'classroom', 'status']


admin.site.register(FoodItems, AdminProduct)
admin.site.register(Users, UserAccounts)
admin.site.register(Categorie, CategoryProduct)
admin.site.register(Order, OrderedItems)
admin.site.register(Cleanliness, CleanlinessData)