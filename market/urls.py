from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('update_user_delivery/', views.update_user_delivery, name='update_user_delivery'),
    path('update_user_payment/', views.update_user_payment, name='update_user_payment'),
    path('item/<item_id>', views.item_info, name='item_info'),
    path('basket/', views.basket, name='basket'),
    path('add_to_basket/<item_id>', views.add_to_basket, name='add_to_basket'),
    path('update_basket_item/', views.update_basket_item, name='update_basket_item'),
    path('buy_basket_items/', views.buy_basket_items, name='buy_basket_items'),
    path('create_items/', views.create_items, name='create_items'),
] 