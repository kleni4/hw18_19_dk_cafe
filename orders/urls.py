from django.urls import path
from . import views

urlpatterns = [
    # Customer URLs
    path('', views.customer_list, name='customer_list'),  # Добавлен корневой URL
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add_form, name='customer_add_form'),
    path('customers/add/submit/', views.customer_add, name='customer_add'),
    path('customers/<int:pk>/edit/', views.customer_edit_form, name='customer_edit_form'),
    path('customers/<int:pk>/edit/submit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    # MenuItem URLs
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/add/', views.menu_item_form, name='menu_item_add_form'),
    path('menu/add/submit/', views.menu_item_add, name='menu_item_add'),
    path('menu/<int:pk>/edit/', views.menu_item_form, name='menu_item_edit_form'),
    path('menu/<int:pk>/edit/submit/', views.menu_item_edit, name='menu_item_edit'),
    path('menu/<int:pk>/delete/', views.menu_item_delete, name='menu_item_delete'),

    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_add_form, name='order_add_form'),
    path('orders/add/submit/', views.order_add, name='order_add'),
    path('orders/<int:pk>/edit/', views.order_edit_form, name='order_edit_form'),
    path('orders/<int:pk>/edit/submit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
]
