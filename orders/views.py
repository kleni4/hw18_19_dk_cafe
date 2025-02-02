from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Customer, MenuItem, Order, OrderItem
from .forms import CustomerForm, MenuItemForm, OrderForm

@require_http_methods(["GET"])
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'orders/customer_list.html', {'customers': customers})


@require_http_methods(["GET"])
def customer_add_form(request):
    form = CustomerForm()
    return render(request, 'orders/customer_form.html', {'form': form})


@require_http_methods(["POST"])
def customer_add(request):
    form = CustomerForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('customer_list')
    return render(request, 'orders/customer_form.html', {'form': form})


@require_http_methods(["GET"])
def customer_edit_form(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(instance=customer)
    return render(request, 'orders/customer_form.html', {'form': form, 'customer': customer})


@require_http_methods(["POST"])
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('customer_list')
    return render(request, 'orders/customer_form.html', {'form': form, 'customer': customer})


@require_http_methods(["POST"])
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customer_list')


@require_http_methods(["GET"])
def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'orders/menu_list.html', {'items': items})


@require_http_methods(["GET"])
def menu_item_form(request, pk=None):
    item = None
    if pk:
        item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(instance=item)
    return render(request, 'orders/menu_form.html', {'form': form, 'item': item})


@require_http_methods(["POST"])
def menu_item_add(request):
    form = MenuItemForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('menu_list')
    return render(request, 'orders/menu_form.html', {'form': form})


@require_http_methods(["POST"])
def menu_item_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST, instance=item)
    if form.is_valid():
        form.save()
        return redirect('menu_list')
    return render(request, 'orders/menu_form.html', {'form': form, 'item': item})


@require_http_methods(["POST"])
def menu_item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    item.delete()
    return redirect('menu_list')


@require_http_methods(["GET"])
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@require_http_methods(["GET"])
def order_add_form(request):
    form = OrderForm()
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'orders/order_form.html', {
        'form': form,
        'menu_items': menu_items
    })


@require_http_methods(["POST"])
def order_add(request):
    form = OrderForm(request.POST)
    if form.is_valid():
        order = form.save()
        menu_items = MenuItem.objects.filter(available=True)
        for item in menu_items:
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity and quantity.isdigit() and int(quantity) > 0:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=int(quantity)
                )
        return redirect('order_list')
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'orders/order_form.html', {
        'form': form,
        'menu_items': menu_items
    })


@require_http_methods(["GET"])
def order_edit_form(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(instance=order)
    menu_items = MenuItem.objects.filter(available=True)
    item_quantities = {
        item.menu_item_id: item.quantity 
        for item in order.orderitem_set.all()
    }
    for item in menu_items:
        item.quantity = item_quantities.get(item.id, 0)
    
    return render(request, 'orders/order_form.html', {
        'form': form,
        'order': order,
        'menu_items': menu_items
    })


@require_http_methods(["POST"])
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST, instance=order)
    if form.is_valid():
        order = form.save()
        OrderItem.objects.filter(order=order).delete()
        menu_items = MenuItem.objects.filter(available=True)
        for item in menu_items:
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity and quantity.isdigit() and int(quantity) > 0:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=int(quantity)
                )
        return redirect('order_list')
    
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'orders/order_form.html', {
        'form': form,
        'order': order,
        'menu_items': menu_items
    })


@require_http_methods(["POST"])
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('order_list')
