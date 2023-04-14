from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import cart,restro,food
from django.contrib import messages

restro_list = restro.objects.all()
food_list = food.objects.all().order_by('food_name')
for i in food_list:
    print(i.restor_id_id)
def index(request):
    global cart_list
    cart_list = cart.objects.filter(user_id= request.user.username)
    cart_list_count = cart_list.count()
    params = {'food_list': food_list, 'cart_list_count': cart_list_count}
    return render (request, "homepage.html", params)

def loginpage(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged In')
        return redirect(index)
    else:
        return render (request, "loginpage.html")

def handlelogin(request):
    if request.method == 'POST':
        login_username = request.POST['login_uname']
        login_password = request.POST['login_pswd']

        user = authenticate(username= login_username, password= login_password)

        if user is not None:
            login(request, user)
            return redirect (index)
        else:
            messages.error(request, 'Invalid Email Address or Password')
            return redirect (loginpage)

    else:
        return redirect(index)
    
def handlelogout(request):
    messages.success(request, f"{request.user.first_name}, Logged Out")
    logout(request)
    return redirect (loginpage)

def registerpage(request):
    return render (request, "registerpage.html")

def handlesignup(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['pswd']
        cpassword = request.POST['cpswd']
        username = email

        if User.objects.filter(email = email).first():
            messages.error(request, 'Email address already exist')
            return redirect(loginpage)

        if password != cpassword:
            messages.error(request, 'Password Not Matched')
            return redirect(loginpage)
        
        createuser = User.objects.create_user(username,email,password)
        createuser.first_name = firstname
        createuser.last_name = lastname
        createuser.save()
        messages.success(request,"Account Created Successfully")
        return redirect(loginpage)

    else:
        return redirect(index)

def mycart(request):
    cart_list = cart.objects.filter(user_id= request.user.username)
    cart_list_count = cart_list.count()

                            ################# Query inside a query ######################
    cart_food_details = cart.objects.filter(user_id = request.user.username).values_list('food_id').all()
    food_details = food.objects.filter(food_id__in = cart_food_details).values()
                            ################# Query inside a query ######################

    params = {'cart_list_count':cart_list_count, 'cart_list':cart_food_details, 'food_details': food_details}
    print (food_details)
    print (cart_list)
    return render (request, "cart.html", params)

def addtocart(request):
    user_id = request.user.username
    food_id = request.POST['food_id']
    quantity = request.POST['quantity']
    try:
        addtocart = cart_list.get(food_id = food_id)
        addtocart.user_id = user_id
        addtocart.food_id = food_id
        addtocart.quantity = addtocart.quantity+int(quantity)
        addtocart.save()
        messages.success(request, 'Your cart has been updated')
        return redirect (index)
    except:
        addtocart = cart()
        addtocart.user_id = user_id
        addtocart.food_id = food_id
        addtocart.quantity = quantity
        addtocart.save()
        messages.success(request, 'New item added to your cart')
        return redirect (index)

def removefromcart(request):
    food_id = request.POST['food_id']
    removefromcart = cart_list.get(food_id = food_id)
    messages.success(request, 'Removed from your cart')
    removefromcart.delete()
    return redirect(index)
