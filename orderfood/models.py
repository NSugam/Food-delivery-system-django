from django.db import models
from django.contrib.auth.models import User

class restro(models.Model):
    restor_id = models.CharField('Resturant ID', max_length=10, primary_key = True)
    restro_name = models.CharField('Resturant Name', max_length=50, default='')
    restro_contact = models.CharField('Contact Number', max_length=50, default='')
    restro_email = models.CharField('Email Address', max_length=50, default='')
    def __str__(self):
        return (f"{self.restro_name}")

class food(models.Model):
    restor_id = models.ForeignKey(restro, default='', on_delete=models.CASCADE)
    food_id = models.CharField('Food ID', max_length=20, primary_key=True)
    food_name = models.CharField('Food Name', max_length=50, default='')
    # food_image = models.ImageField(upload_to= "orderfood/images", default='')
    food_category = models.CharField('Food Category', max_length=50, default='')
    food_type = models.CharField('Food Type', max_length=50, default='')
    food_price = models.IntegerField('Food Price', default = 00)
    delivery_time = models.IntegerField('Delivery Time', default = 00)
    def __str__(self):
        return (f"{self.food_name}")
    
class cart(models.Model):
    user_id = models.CharField('User ID', max_length=50)
    food_id = models.CharField('Food ID', default='', max_length=50)
    quantity = models.IntegerField('Quantity', default = 1)
    def __str__(self):
        return (f"{self.user_id}")

class order(models.Model):
    order_id = models.CharField('Order ID', max_length=50, primary_key = True, default='')
    user_id = models.CharField('User ID', max_length=50)
    food_id = models.ForeignKey(food, default='', on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity', default = 1)
    delivery_location = models.CharField('Delivery Location', max_length=100, default='')
    delivery_status = models.CharField('Delivery Status', max_length=50, default="Pending Approval")



