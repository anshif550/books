from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    image = models.ImageField(null=True,blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title
    

class Cart(models.Model):
    image = models.ImageField(null=True,blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="cart")
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="cart")
    quantity = models.PositiveIntegerField(default=1)



    def __str__(self):
        return self.title
    
class Contact(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

