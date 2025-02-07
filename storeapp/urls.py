from django.urls import path
from .views import *

urlpatterns = [
    path('',index, name='home'),
    path('products/', products_view, name='products_view'),
    path('category/<str:pk>/', category, name='categories'),

    path('registration/', registeruserview, name='registeruser'),
    path('login/', loginuserview, name='loginuser'),
    path('profile/', userprorfileview, name='profile'),
    path('logout/', logoutuser, name='logout'),
    path('add-basket/<str:pk>/', add_basket_view, name='add_basket'),
    path('delete-basket/<str:pk>/', delete_basket_view, name='delete_basket'),
    path('create-order/', create_oreder_view, name='create_order'),
    path('success/', success_view, name='success'),
    path('orders/', orders_view, name='orders'),
    path('order/<str:pk>/', order_single_view, name='order'),

    path('admin-panel/', adminpanel, name='admin_panel'),
    path('change-status/<str:pk>/', change_status, name='change_status'),
    path('edit-order/<str:pk>/', edit_order, name='edit_order'),
    path('delete-order/<str:pk>/', delete_order_view, name='delete_order'),
    path('order-category/<str:status>/', order_category_view, name='order_category'),

]
