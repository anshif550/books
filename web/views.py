from django.shortcuts import render, redirect, get_object_or_404 ,reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from Store.models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from users.models import User
from customer.models import*
from django.http import JsonResponse


@login_required(login_url='/login/')
def index(request):
    categories = Category.objects.all()
    authors = Author.objects.all()
    books = Book.objects.all()
    products = Product.objects.all()[:5]

    context = {
        'author': authors,
        'books': books,
        'category': categories,
        'products': products,
    }

    return render(request, "web/index.html", context=context)


@login_required(login_url='/login/')
def allproduct(request):
    """View displaying all products and authors."""
    products = Product.objects.all()
    authors = Author.objects.all()

    context = {
        'products': products,
        'author': authors,
    }

    return render(request, "web/allproduct.html", context=context)


@login_required(login_url='/login/')
def singlebook(request, id):

    products = get_object_or_404(Product, id=id) 

    context = {
        'products': products,
    }

    return render(request, "web/singlebook.html", context=context)



@login_required(login_url='/login/')
def cart(request):

    customer = get_object_or_404(Customer, user=request.user)
    cart_items = Cart.objects.filter(customer=customer)
    total_price = sum(item.price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'web/cart.html', context=context)


@login_required(login_url='/login/')
def contact(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        send_mail(
            subject,
            f"Message from {name} ({email}):\n\n{message}",
            'your_email@example.com',  # Replace with your email
            ['recipient@example.com'],  # Replace with recipient's email
        )

        return HttpResponse("Thank you for your message!")

    return render(request, "web/contact.html")

@login_required(login_url='/login/')
def add_cart(request, id):
    user = request.user
    # Ensure the Customer object exists for the logged-in user
    customer, created = Customer.objects.get_or_create(user=user)

    # Fetch the product
    product = get_object_or_404(Product, id=id)

    # Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        price=product.price,
        quantity=1
    )
    cart_item.save()

    return redirect('web:cart')


def remove_cart_item(request, id):
    if not request.user.is_authenticated:
        return redirect('web:login')
    
    customer = get_object_or_404(Customer, user=request.user)
    cart_item = get_object_or_404(Cart, id=id, customer=customer)
    cart_item.delete()
    return redirect('web:cart')


def update_cart_quantity(request, id):
    """Update the quantity of a cart item and adjust the price accordingly."""
    if request.method == "POST":
        customer = get_object_or_404(Customer, user=request.user)
        cart_item = get_object_or_404(Cart, id=id, customer=customer)

        try:
            new_quantity = int(request.POST.get("quantity", 1))
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.price = cart_item.product.price * new_quantity  # Update total price
                cart_item.save()
            else:
                cart_item.delete()  # Remove item if quantity is set to 0
        except ValueError:
            return HttpResponse("Invalid quantity", status=400)

    return redirect('web:cart')

@login_required(login_url='/login/')
def chekout(request):
    # Get the logged-in user
    user = request.user
    customer = Customer.objects.get(user=user)
    
    # Get the items in the cart
    cart_items = Cart.objects.filter(customer=customer)
    total_price = sum(item.price * item.quantity for item in cart_items)
    
    if request.method == "POST":
        # Handle the form submission
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        # Create a new Order (you should have an Order model)
        order = Order.objects.create(
            customer=customer,
            name=name,
            email=email,
            address=address,
            total_price=total_price,
            payment_method=payment_method,  # Cash on Delivery
            status="Pending"  # You can set order status based on your workflow
        )

        # Move cart items to the order (optional, depends on your order flow)
        for item in cart_items:
            order.save  # Assuming you have a relation with the Product model
        
        cart_items.delete()

        return redirect('web:order_success', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'web/chekout.html', context)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    context = {
        'order': order,
    }

    return render(request, 'web/order_success.html', context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('web:login'))

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('web:index'))
        else:
            context = {
                'error': True,
                'message' : 'invalid Email or password'
            }
            return render(request, 'web/login.html', context)
    else:
        return render(request, 'web/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password') 

        if User.objects.filter(email=email).exists():
            context = {
                'error': True,
                'message' : 'Email already exists'
            }
            return render(request, 'web/register.html', context=context)
            
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_customer=True
            )
            user.save()
            customer = Customer.objects.create(
                user=user
            )
            customer.save()
            return HttpResponseRedirect(reverse('web:login'))
    else:
        return render(request, 'web/register.html') 
    
def categories(request, category_id=None):
    # Fetch all categories
    categories = Category.objects.all()

    # Fetch products filtered by category (if provided), otherwise fetch all
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    # Prepare the context for rendering
    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'web/categories.html', context=context)

def newrelease(request, category_id=None):
    # Fetch all categories
    categories = Category.objects.all()

    # Fetch products filtered by category (if provided), otherwise fetch all
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    # Prepare the context for rendering
    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'web/newrelease.html', context=context)

def preorder(request, category_id=None):
    # Fetch all categories
    categories = Category.objects.all()

    # Fetch products filtered by category (if provided), otherwise fetch all
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    # Prepare the context for rendering
    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'web/preorder.html', context=context)

def ofered(request, category_id=None):
    # Fetch all categories
    categories = Category.objects.all()

    # Fetch products filtered by category (if provided), otherwise fetch all
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    # Prepare the context for rendering
    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'web/ofered.html', context=context)


@login_required(login_url='/login/')
def explore(request):


    return render(request, "web/explore.html")


@login_required
def my_orders(request):
    """
    View to display all orders for the logged-in user.
    """
    orders = Order.objects.filter(customer__user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'web/my_orders.html', context)

@login_required
def order_detail(request, order_id):
    """
    View to display details of a specific order.
    """
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    context = {
        'order': order
    }
    return render(request, 'web/order_detail.html', context)

@login_required
def create_order(request):
    """
    View to create a new order.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer  # Assuming a `Customer` model with a OneToOneField to User
            order.save()
            return HttpResponseRedirect(reverse('order_detail', args=[order.id]))
    else:
        form = OrderForm()
    
    context = {
        'form': form
    }
    return render(request, 'web/create_order.html', context)


