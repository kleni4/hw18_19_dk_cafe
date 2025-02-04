from django.urls import path
from .views import (
    CustomerListView, 
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    MenuListView,
    MenuItemCreateView,
    MenuItemUpdateView,
    MenuItemDeleteView,
    OrderListView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView
)

urlpatterns = [
    # Customer URLs
    path('', CustomerListView.as_view(), name='customer_list'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/add/', CustomerCreateView.as_view(), name='customer_add_form'),
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit_form'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    
    # MenuItem URLs
    path('menu/', MenuListView.as_view(), name='menu_list'),
    path('menu/add/', MenuItemCreateView.as_view(), name='menu_item_add_form'),
    path('menu/<int:pk>/edit/', MenuItemUpdateView.as_view(), name='menu_item_edit_form'),
    path('menu/<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu_item_delete'),
    
    # Order URLs
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/add/', OrderCreateView.as_view(), name='order_add_form'),
    path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_edit_form'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
]
