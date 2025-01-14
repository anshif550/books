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
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'), 
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.categories, name='category_products'), 
    path('newrelease/', views.newrelease, name='newrelease'),
    path('newrelease/<int:category_id>/', views.newrelease, name='category_products'), 
    path('preorder/', views.preorder, name='preorder'),
    path('preorder/<int:category_id>/', views.preorder, name='category_products'),
    path('ofered/', views.ofered, name='ofered'),
    path('ofered/<int:category_id>/', views.ofered, name='category_products'), 
    path('explore/', views.explore, name='explore'),
    path('my_orders/',views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('create-order/', views.create_order, name='create_order'),
] 
   
    


