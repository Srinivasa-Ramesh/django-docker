from django.shortcuts import render ,redirect
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
    cart_item = Product.objects.all()
    return render(request,'users/cart.html', {'cart_item': cart_item})

def add_to_cart(request, product_id):
    """Add product to the cart stored in session"""
    cart = request.session.get('cart', {})  # Get cart or empty dict

    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Increase quantity if already in cart
    else:
        cart[str(product_id)] = 1  # Add new product with quantity 1

    request.session['cart'] = cart  # Save back to session
    return redirect('cart')  # Redirect to cart page

def cart_page(request):
    """Display cart items"""
    cart = request.session.get('cart', {})  # Get cart from session
    products = Product.objects.filter(id__in=cart.keys())  # Fetch products

    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'subtotal': product.price * cart[str(product.id)]
        })

    total_price = sum(item['subtotal'] for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})