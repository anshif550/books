from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("allproduct/", views.allproduct, name="allproduct"),
    path("singlebook/<int:id>/", views.singlebook, name="singlebook"),
    path("cart/", views.cart, name="cart"),
    path("contact/", views.contact, name="contact"),
    path("checkout/", views.checkout, name="checkout"),
]