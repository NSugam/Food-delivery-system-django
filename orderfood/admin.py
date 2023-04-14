from django.contrib import admin
from .models import order, restro, food, cart

class CARTLIST(admin.ModelAdmin):
    list_display = ['user_id','food_id', 'quantity']

class FOODLIST(admin.ModelAdmin):
    list_display = ['food_name', 'food_id']

admin.site.register(order)
admin.site.register(cart, CARTLIST)
admin.site.register(restro)
admin.site.register(food, FOODLIST)
