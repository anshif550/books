from django.shortcuts import render, reverse, redirect
from customer.models import *
from django.http import HttpResponseRedirect, HttpResponse
from manager.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from main.functions import generate_form_errors
from main.decorators import allow_manager
from Store.models import*
def index(request):       
   
    return render(request, 'manager/index.html')        


def categories(request):         
    instances = Category.objects.all()

    context = {
        'instances': instances
    }
    return render(request, 'manager/categories.html',context=context)  

def category_add(request):
    if request.method == 'POST':   
        form = Categoryform(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(reverse('manager:categories'))
        else:
            message = generate_form_errors(form)
    else:
        form = Categoryform()
        message = None

    context = {
        "error": message is not None,
        "message": message,
        "form": form,
    }
    return render(request, 'manager/category_add.html', context=context)


def category_delete(request,id):
    instance = Category.objects.get(id=id)
    
    instance.delete()

    return HttpResponseRedirect(reverse('manager:categories'))



def products(request):         
    instances = Product.objects.all()

    context = {
        'instances': instances
    }
    return render(request, 'manager/products.html',context=context)  


def products_add(request):
    if request.method == 'POST':   
        form = ProductForm(request.POST, request.FILES)  # Use ProductForm instead of Categoryform
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()  # Save the new product instance
            return HttpResponseRedirect(reverse('manager:products'))
        else:
            message = generate_form_errors(form)
    else:
        form = ProductForm()  # Initialize the form for GET requests
        message = None

    context = {
        "error": message is not None,
        "message": message,
        "form": form,
    }

    return render(request, 'manager/products_add.html', context=context)

def products_delete(request,id):
    instance = Product.objects.get(id=id)
    
    instance.delete()

    return HttpResponseRedirect(reverse('manager:products'))

