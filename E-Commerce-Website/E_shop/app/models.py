from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name



class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Product(models.Model):

    Availability = (('In Stock','In Stock'),('Out Of Stock','Out Of Stock'))

    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=False,default='')
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE,null=False,default='')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=100)
    disc = models.CharField(max_length=150)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    Availability = models.CharField(choices=Availability,null=True, max_length=100)
    date = models.DateField(auto_now_add=True)

    # Additional Fields
    weight = models.CharField(max_length=50, null=True, blank=True)  # e.g., "1kg", "500g"
    discription = models.TextField(max_length=200, null=True, blank=True)  # Nutritional details
    ingredients = models.TextField(null=True, blank=True)  # Ingredients for edible items

    shelf_life = models.CharField(max_length=100, null=True, blank=True)  # e.g., "6 months"
    packaging_type = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Plastic Bag", "Carton"  # Discount percentage
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # Average customer rating
    reviews_count = models.IntegerField(default=0)  # Total number of reviews
    stock_quantity = models.IntegerField(default=0)  # Quantity available in stock
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)  # Unique Stock Keeping Unit
    is_featured = models.BooleanField(default=False)  # Highlighted product for promotions
    is_organic = models.BooleanField(default=False)  # Flag for organic products

    # Methods
    def discounted_price(self):
        """Calculate the discounted price."""
        return self.price - (self.price * self.discount // 100)


    def __str__(self):
        return self.name


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email',error_messages={'exist': 'This Already Exists'})

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_message['exists'])
        return self.cleaned_data['email']



class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email



class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=100, default='')
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
