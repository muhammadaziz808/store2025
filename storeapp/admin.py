from django.contrib import admin
from .models import *

@admin.register(TovarModel)
class AdminTovar(admin.ModelAdmin):
    list_display = ['image','name','price','about','category']

@admin.register(CategoryModel)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Userprofile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username']

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'owner']


@admin.register(BasketModl)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['product','owner','count','ordered']