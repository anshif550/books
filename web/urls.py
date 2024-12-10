from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),  # Homepage
    path("allproduct/", views.allproduct, name="allproduct"),  # All Products
    path("singlebook/<int:id>/", views.singlebook, name="singlebook"),  # Single Book Details
    path("cart/", views.cart, name="cart"),  # User Cart
    path("contact/", views.contact, name="contact"),  # Contact Page
    path("chekout/", views.chekout, name="chekout"),  # Checkout Process
    path("add-cart/<int:id>/", views.add_cart, name="add_cart"),
    path("remove-cart-item/<int:id>/", views.remove_cart_item, name="remove_cart_item"),
    path("update-cart/<int:id>/", views.update_cart_quantity, name="update_cart_quantity"),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

]