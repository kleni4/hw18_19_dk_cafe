from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='order_list', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),  # Убираем prefix 'orders/'
]
