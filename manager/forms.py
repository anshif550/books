from django import forms
from Store.models import *
from users.models import User
from customer.models import *




class Categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'category name'}),
       }
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'image', 'category', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product title'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'total_price', 'payment_method']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Address', 'rows': 3}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Price'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'address': 'Shipping Address',
            'total_price': 'Total Amount',
            'payment_method': 'Payment Method',
        }       
