
from django.urls import path
from manager import views

app_name="web"

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/",views.categories, name="categories"),
    path("category_add/",views.category_add, name="category_add"),
    path("category_delete/<int:id>/", views.category_delete, name="category_delete"),
     path('products/add/', views.products_add, name='products_add'),
    path("products/",views.products, name="products"),
     path("products_delete/<int:id>/", views.products_delete, name="products_delete"),


]