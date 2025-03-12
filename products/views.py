from django.shortcuts import render ,redirect,get_object_or_404
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from .models import Product


def register(request):
    if request.method == "POST":
          form = UserCreationForm(request.POST)
          if form.is_valid():
              user = form.save()
              login(request,user)
              return redirect('home')
    else:
           form = UserCreationForm()
    return render(request,'users/register.html',{'form':form})

def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        messages.error(request, "Username and password are required")
    return render(request,'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('register')

def user_home(request):
    products = Product.objects.all()

    for product in products:
        # fetch values as numbers
        original_price = float(product.price)
        discounted = float(product.disc)
        discount_amount = (discounted / 100) * original_price
        product.final_price = round (original_price - discount_amount)

    return render(request,'users/home.html',{'products':products})


def cart(request):
    id_product= Product.objects.all()
    return render(request, "users/cart.html", {"id_product": id_product})