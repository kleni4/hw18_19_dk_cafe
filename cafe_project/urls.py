from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_orders(request):
    return redirect('order_list')  # Используем name вместо хардкода пути

urlpatterns = [
    path('', redirect_to_orders, name='home'),
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),  # Убираем prefix 'orders/'
]
