from django.contrib import admin
from .models import Customer, MenuItem, Order, OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone_number')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_filter = ('category', 'available', 'name')
    search_fields = ('name', 'description')
    list_editable = ('available', 'price')
    ordering = ('category', 'name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ('menu_item',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at', 'updated_at', 'get_total_price')
    list_filter = ('created_at', 'status')
    search_fields = ('customer__name', 'id')
    raw_id_fields = ('customer',)
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    
    def get_total_price(self, obj):
        return f"{obj.total_price} тг."
    get_total_price.short_description = 'Total Price'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'get_item_total')
    list_filter = ('quantity',)
    search_fields = ('order__id', 'menu_item__name')
    raw_id_fields = ('order', 'menu_item')
    
    def get_item_total(self, obj):
        return f"{obj.menu_item.price * obj.quantity} тг."
    get_item_total.short_description = 'Total'
