from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from .models import Users, FoodItems, Order, Categorie, Cleanliness
import datetime 
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from U2H.auth import auth_middleware


# Create your views here.

def index(request):
    return render (request, 'index.html')

# Create your views here.

#Function for registration of new users (students,teachers)
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        prn = request.POST['prn']
      
        if Users.objects.filter(email=email).exists():
            messages.info(request,'E-mail ID already in use')
            return redirect('register')
        elif Users.objects.filter(prn=prn).exists():
            messages.info(request,'This PRN no. already exists')
            return redirect('register')
        else:
            user = Users(prn=prn, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            messages.info(request, 'Now you are ready to log in!')
            return redirect('login')        

    else:  
        return render(request,'register.html')

#Function for login of users (students,teachers)
def login(request):
    
    
    if request.method=='POST':
    #     return render(request, 'login.html')
    # else:
        password = request.POST.get('password')
        prn_email = request.POST.get('prn')
        clean_role = 'Cleanliness'
        canteen_role = 'Canteen'

        if Users.objects.filter(email=prn_email).exists():
            user = Users.get_users_by_email(prn_email)
        elif Users.objects.filter(prn=prn_email).exists():
            user = Users.get_users_by_prn(prn_email)
        else:
            user = ""
        # error_message=None
        
        # if user:
        #     flag = Users.check_pwd(password)
        #     print(flag)
            # if flag:
            #     return redirect('dashboard')
            # else:
            #     error_message="Invalid Credentials"
        # else:
        #     error_message="Invalid Credentials"

        # return render(request,'login.html',{'error':error_message})

        if Users.objects.filter(email=prn_email).exists() or Users.objects.filter(prn=prn_email).exists():
            if Users.objects.filter(password=password):                          
                request.session['user'] = user.id
                if user.role==clean_role:
                    return redirect('cleanliness_admin')
                elif user.role==canteen_role:
                    return redirect('canteen_admin')
                else:
                    return redirect('dashboard')
            else:
                messages.info(request, 'Invalid Credentials .. !!')
                return redirect('login')
        else:
            messages.info(request, 'Invalid Credentials .. !!')
            return redirect('login')        

    else:  
        return render(request,'login.html')

def about(request):
    return render (request, 'about.html')

def contact(request):
    return render (request, 'contact.html')

@auth_middleware
def dashboard(request):
    print(request.session.get('user'))
    return render (request, 'dashboard.html')

@auth_middleware
def canteen(request):

    if request.method=='POST':
        item_id=request.POST.get('item_id')
        remove = request.POST.get('remove')

        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(item_id)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(item_id)
                    else:
                        cart[item_id]= quantity - 1
                else:
                    cart[item_id]= quantity + 1
            else:
                cart[item_id]=1
        else:
            cart={}
            cart[item_id]=1

        request.session['cart'] = cart
        return redirect('canteen')

    if request.method=='GET':
        category = Categorie.get_all_categories()
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        items = None
        # request.session.get('cart').clear()
        category_ID=request.GET.get('category')
        if category_ID:
            items = FoodItems.get_all_items_by_category_id(category_ID)
        else:
            items = FoodItems.get_all_items()
        data={}
        data['items'] = items
        data['category'] = category
        return render(request, 'canteen.html', data)


@auth_middleware
def cart(request):
    if request.method=='GET':
        item_ids = list(request.session.get('cart').keys())
        food_items = FoodItems.get_items_by_id(item_ids)
        return render(request, 'cart.html', {'food_items':food_items})
        


def logout(request):
    request.session.clear()
    return redirect('login')

@auth_middleware
def checkout(request):
    if request.method=='POST':
        current_date_and_time = datetime.datetime.now()
        hours = 1
        hours_added = datetime.timedelta(hours = hours)
        future_date_and_time = current_date_and_time + hours_added
        
        datetime_object = request.POST.get('delivery_datetime')
        delivery_datetime = datetime.datetime.strptime(datetime_object, "%Y-%m-%dT%H:%M")

        order_object = Order.get_max_order_id()

        if order_object is None:
            recent_order_id=1001
        else:
            recent_order_id = order_object + 1

        user = request.session.get('user')
        cart = request.session.get('cart')
        food_items = FoodItems.get_items_by_id(list(cart.keys()))

        if delivery_datetime >= future_date_and_time:           
            for item in food_items:
                order = Order(  order_id = recent_order_id,
                                user = Users(id = user),
                                food_item = item,
                                total_price = item.price,
                                quantity = cart.get(str(item.id)),
                                delivery_datetime = delivery_datetime

                            )
                order.save()
            request.session['cart'] = {}
            messages.info(request, 'Your order has placed successfully')
            return redirect('cart')
        else:
            messages.info(request, 'Delivery Time should be atleast 1 hour later')
            return redirect('cart')

@auth_middleware
def orders(request):
    if request.method=='GET':
        user = request.session.get('user')
        order = Order.get_orders_by_user(user)
        return render(request, 'orders.html', {'order_list':order})

@auth_middleware
def cleanliness(request):
    if request.method=="POST":
        user = request.session.get('user')
        building_name = request.POST.get('building_name')
        classroom = request.POST.get('classroom')
        description = request.POST.get('description')
        
        cleanliness_data = Cleanliness( user=Users(id = user),
                                        building_name=building_name,
                                        classroom=classroom,
                                        description=description)

        cleanliness_data.save()
        messages.info(request, 'Complaint Recorded Successfully')
        return redirect('cleanliness')
    else:
        return render(request,'cleanliness.html')

@auth_middleware
def cleanliness_admin(request):
    user_id = request.session.get('user')
    user_obj = Cleanliness.get_name_by_user(user_id)
    name = user_obj.first_name+" "+user_obj.last_name 
    #print(user_id, user_obj, name)

    if request.method=="GET":
        complaint_list = Cleanliness.get_pending_complaint()
        return render(request, 'cleanliness_admin.html', {'name':name, 'complaint_list':complaint_list})
   
    if request.method=="POST":
        complaint_id = request.POST.get('complaint_id')
        complaint_list = Cleanliness.set_complaint_status(complaint_id)
        return render(request, 'cleanliness_admin.html', {'name':name, 'complaint_list':complaint_list})

@auth_middleware
def canteen_admin(request):
    user_id = request.session.get('user')
    user_obj = Order.get_name_by_user(user_id)
    name = user_obj.first_name+" "+user_obj.last_name

    if request.method=="GET":
         order_list = Order.group_by_orders()
         return render(request, 'canteen_admin.html', {'name':name, 'order_list':order_list})

    # if request.method=="POST":
    #     delivery_datetime = request.POST.get('delivery_datetime')
    #     userid = request.POST.get('user')
    #     return render(request, 'view_order.html', {'delivery_datetime':delivery_datetime, 'userid':userid})

@auth_middleware
def view_order(request):
    if request.method=="GET":
        user_id = request.session.get('user')
        user_obj = Order.get_name_by_user(user_id)
        name = user_obj.first_name+" "+user_obj.last_name

        order_id =request.GET.get('order_id')
        order_list = Order.get_orders_from_order_id(order_id)
        student_name = order_list[0].user.first_name+" "+order_list[0].user.last_name
        student_prn = order_list[0].user.prn
        delivery_datetime = order_list[0].delivery_datetime

        data = {}
        data['student_name'] = student_name
        data['student_prn'] = student_prn
        data['delivery_datetime'] = delivery_datetime

        return render(request, 'view_order.html', {'order_id':order_id, 'order_list':order_list, 'data':data, 'name':name})

    if request.method=="POST":
        order_id =request.POST.get('order_id')
        status = Order.set_order_status(order_id)
        return redirect('canteen_admin')

@auth_middleware
def view_complaints(request):
    if request.method=="GET":
        user = request.session.get('user')
        complaints_list = Cleanliness.get_all_complaints_by_userID(user)
        return render(request,'view_complaints.html', {'complaints_list':complaints_list})
