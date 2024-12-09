from django.shortcuts import render
from Store.models import*
from django.core.mail import send_mail
from django.http import HttpResponse

def index(request):
    categories = Category.objects.all()
    authors = Author.objects.all()
    books = Book.objects.all()
    products = Product.objects.all()

    
    context = {
        'author':authors,
        'books':books,
        'category':categories,
        'products':products,
    }

    return render(request, "web/index.html",context=context)

def allproduct(request):
    products = Product.objects.all()
    authors = Author.objects.all()

    context = {
        'products':products,
        'author':authors,
    }

    
    return render(request, "web/allproduct.html",context=context)


def singlebook(request,id):
    products = Product.objects.get(id=id)

    
    context = {
        'products':products,
    }

    
    return render(request, "web/singlebook.html",context=context)

def cart(request):

    
    return render(request, "web/cart.html")


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Send email
        send_mail(
            subject,
            f"Message from {name} ({email}):\n\n{message}",
            'anshffyz@gmail.com',  # Replace with your email
            ['recipient@example.com'],  # Replace with recipient's email
        )

        return HttpResponse("Thank you for your message!")

    return render(request,"web/contact.html")


def checkout(request):


    return render(request, "web/checkout.html")



