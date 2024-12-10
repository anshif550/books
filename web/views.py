from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from Store.models import *
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    """Homepage view displaying categories, authors, books, and products."""
    categories = Category.objects.all()
    authors = Author.objects.all()
    books = Book.objects.all()
    products = Product.objects.all()

    context = {
        'author': authors,
        'books': books,
        'category': categories,
        'products': products,
    }

    return render(request, "web/index.html", context=context)


def allproduct(request):
    """View displaying all products and authors."""
    products = Product.objects.all()
    authors = Author.objects.all()

    context = {
        'products': products,
        'author': authors,
    }

    return render(request, "web/allproduct.html", context=context)


def singlebook(request, id):

    products = get_object_or_404(Product, id=id) 

    context = {
        'products': products,
    }

    return render(request, "web/singlebook.html", context=context)


@login_required
def cart(request):

    customer = get_object_or_404(Customer, user=request.user)
    cart_items = Cart.objects.filter(customer=customer)
    total_price = sum(item.price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'web/cart.html', context=context)


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







@login_required
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

@login_required
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





