from django.db import models
import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.query import QuerySet
from django.db.models import Max
# Create your models here.

class Users(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.TextField()
    password = models.CharField(max_length = 100)
    prn = models.CharField(max_length = 100)
    role = models.TextField(default='Student')
    
    @staticmethod
    def get_users_by_email(data):
        try:
            return Users.objects.get(email=data)
        except:
            return False

    @staticmethod
    def get_users_by_prn(data):
        try:
            return Users.objects.get(prn=data)
        except:
            return False

    # @staticmethod
    # def check_pwd(pwd):
    #     chk = check_password(pwd,Users.password)
    #     if chk:
    #         return True
    #     else:
    #         return False



class Categorie(models.Model):
    category_name=models.CharField(max_length = 100)

    def __str__(self):
        return self.category_name

    @staticmethod
    def get_all_categories():
        return Categorie.objects.all()
    
    @staticmethod
    def get_category_by_id(category_id):
        return Categorie.objects.get(id=category_id)

class FoodItems(models.Model):
    item_name = models.CharField(max_length = 100)
    price = models.IntegerField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    item_img = models.ImageField(upload_to='pics')

    @staticmethod
    def get_all_items():
        return FoodItems.objects.all()

    @staticmethod
    def get_all_items_by_category_id(category_id):
        if category_id:
            return FoodItems.objects.filter(category = category_id)
        else:
            return FoodItems.get_all_items()
    
    @staticmethod
    def get_items_by_id(item_id):
        return FoodItems.objects.filter(id__in=item_id)

class Order(models.Model):
    order_id = models.IntegerField(default=1)
    food_item = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    date = models.DateTimeField(default=datetime.datetime.now)
    delivery_datetime = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(default=False)

    @staticmethod
    def get_orders_by_user(user_id):
        return Order.objects.filter(user = user_id).order_by('-date')

    @staticmethod
    def get_name_by_user(user_id):
        return Users.objects.get(id = user_id)

    @staticmethod
    def get_pending_orders():
        return Order.objects.filter(status = False).order_by('-delivery_datetime')

    @staticmethod
    def group_by_orders():
        return Order.objects.filter(status=False).distinct('order_id')

    @staticmethod
    def set_order_status(oid):
        order = Order.objects.filter(order_id=oid)
        for o in range(len(order)):
            order[o].status = True
            order[o].save()        
        # order.status = True
        # order.save()
        return True

    @staticmethod
    def get_max_order_id():
        order_ids = Order.objects.aggregate(max_order_id = Max('order_id'))
        # id_value = order_ids.get('max_order_id') + 1
        print("Model",order_ids)
        return order_ids.get('max_order_id')

    @staticmethod
    def get_orders_from_order_id(oid):
        return Order.objects.filter(order_id=oid)

class Cleanliness(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    building_name = models.TextField()
    classroom = models.TextField()
    description = models.TextField()
    status = models.BooleanField(default=False)

    @staticmethod
    def get_name_by_user(user_id):
        return Users.objects.get(id = user_id)

    @staticmethod
    def get_pending_complaint():
        return Cleanliness.objects.filter(status = False)

    @staticmethod
    def set_complaint_status(complaint_id):
        complaint = Cleanliness.objects.get(id=complaint_id)
        complaint.status = True
        complaint.save()
        return Cleanliness.objects.filter(status = False)

    @staticmethod
    def get_all_complaints_by_userID(userid):
        return Cleanliness.objects.filter(user=userid).order_by('-id')