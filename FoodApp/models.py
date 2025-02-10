from django.db import models
import os,datetime
from django.contrib.auth.models import User
# Create your models here.

def get_file_path(instance,filename):
    original_filename=filename
    nowTime=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime,original_filename)
    return os.path.join('uploads/',filename)

def get_image_path(instance,filename):
    original_filename=filename
    nowTime=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime,original_filename)
    return os.path.join('image/',filename)


class Category(models.Model):
    slug=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=get_file_path,null=True,blank=True)
    descriptions=models.TextField(max_length= 500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=Trending")
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description=models.TextField(max_length= 500,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name)
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug=models.CharField(max_length=150,null=False,blank=False)
    name=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=get_image_path,null=True,blank=True)
    small_description=models.CharField(max_length= 250,null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    descriptions=models.TextField(max_length= 500,null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=Trending")
    trending=models.BooleanField(default=False,help_text="0=default,1=Trending")
    tag=models.CharField(max_length=150,null=False,blank=False)
    meta_title=models.CharField(max_length=150,null=False,blank=False)
    meta_keywords=models.CharField(max_length=150,null=False,blank=False)
    meta_description=models.TextField(max_length= 500,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=550,null=False)
    lname = models.CharField(max_length=550,null=False)
    email = models.EmailField(max_length=254,null=False)
    phone = models.CharField(max_length=50,null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=550,null=False)
    state = models.CharField(max_length=550,null=False)
    country = models.CharField(max_length=550,null=False)
    pincode = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=550,null=False)
    payment_id = models.CharField(max_length=550,null=True)
    orderstatus = (
        ('Pending','pending'),
        ('Out for Shipping','Out for Shipping'),
        ('Completed','Completed'),
    )
    status = models.CharField(max_length=550,choices=orderstatus,default='Pending')
    messages = models.TextField(null=True)
    trackno = models.CharField(max_length=5000,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f'{self.id} - {self.trackno}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    qty = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.order.id}-{self.order.trackno}'
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=50,null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=550,null=False)
    state = models.CharField(max_length=550,null=False)
    country = models.CharField(max_length=550,null=False)
    pincode = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username