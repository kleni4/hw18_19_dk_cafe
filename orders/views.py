# https://www.geeksforgeeks.org/get_object_or_404-method-in-django-models/
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Customer, MenuItem, Order, OrderItem
from .forms import CustomerForm, MenuItemForm, OrderForm
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

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

# Customer Views
class CustomerListView(TemplateView):
    template_name = 'orders/customer_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        return context

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'orders/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'orders/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customer_list')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# MenuItem Views
class MenuListView(TemplateView):
    template_name = 'orders/menu_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = MenuItem.objects.all()
        category_filter = self.request.GET.get('category')
        
        # Фильтруем блюда по категории если она указана
        if category_filter and category_filter != 'all':
            items = items.filter(category=category_filter)
            
        context['items'] = items
        context['current_category'] = category_filter
        
        # Получаем кол-во блюд в каждой кат.
        context['categories_count'] = {
            'all': MenuItem.objects.count(),
            'drinks': MenuItem.objects.filter(category='drinks').count(),
            'main': MenuItem.objects.filter(category='main').count(),
            'desserts': MenuItem.objects.filter(category='desserts').count(),
        }
        return context

class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'orders/menu_form.html'
    success_url = reverse_lazy('menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = None  # для нового блюда
        return context

class MenuItemUpdateView(UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'orders/menu_form.html'
    success_url = reverse_lazy('menu_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.object  # передаем существующий объект в контекст
        return context

class MenuItemDeleteView(DeleteView):
    model = MenuItem
    success_url = reverse_lazy('menu_list')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Order Views
class OrderListView(TemplateView):
    template_name = 'orders/order_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()
        status_filter = self.request.GET.get('status')
        
        # тчк останова (удалить)
        print(f"Status filter: {status_filter}")
        print(f"All orders statuses: {[order.status for order in orders]}")
        
        # Фильтр заказы по статус
        if status_filter and status_filter != 'all':
            filtered_orders = orders.filter(status=status_filter)
            print(f"Filtered orders count: {filtered_orders.count()}")
            orders = filtered_orders
            
        context['orders'] = orders
        context['current_status'] = status_filter
        return context

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.filter(available=True)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Обработка элементов заказа
        for key, value in self.request.POST.items():
            if key.startswith('quantity_') and value and int(value) > 0:
                item_id = key.split('_')[1]
                menu_item = MenuItem.objects.get(pk=item_id)
                OrderItem.objects.create(
                    order=self.object,
                    menu_item=menu_item,
                    quantity=int(value)
                )
        return response

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.filter(available=True)
        for item in context['menu_items']:
            order_item = OrderItem.objects.filter(order=self.object, menu_item=item).first()
            item.quantity = order_item.quantity if order_item else 0
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Обновление элементов заказа
        OrderItem.objects.filter(order=self.object).delete()
        for key, value in self.request.POST.items():
            if key.startswith('quantity_') and value and int(value) > 0:
                item_id = key.split('_')[1]
                menu_item = MenuItem.objects.get(pk=item_id)
                OrderItem.objects.create(
                    order=self.object,
                    menu_item=menu_item,
                    quantity=int(value)
                )
        return response

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# FormView для форм
class CustomerFormView(FormView):
    template_name = 'orders/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(Customer, pk=self.kwargs['pk'])
            kwargs['instance'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'object'):
            context['customer'] = self.object
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class MenuItemFormView(FormView):
    template_name = 'orders/menu_form.html'
    form_class = MenuItemForm
    success_url = reverse_lazy('menu_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(MenuItem, pk=self.kwargs['pk'])
            kwargs['instance'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'object'):
            context['item'] = self.object
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class OrderFormView(FormView):
    template_name = 'orders/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(Order, pk=self.kwargs['pk'])
            kwargs['instance'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.filter(available=True)
        if hasattr(self, 'object'):
            context['order'] = self.object
            for item in context['menu_items']:
                order_item = OrderItem.objects.filter(order=self.object, menu_item=item).first()
                item.quantity = order_item.quantity if order_item else 0
        return context

    def form_valid(self, form):
        order = form.save()
        
        # Обработка элементов заказа
        if hasattr(self, 'object'):
            OrderItem.objects.filter(order=self.object).delete()
            
        for key, value in self.request.POST.items():
            if key.startswith('quantity_') and value and int(value) > 0:
                item_id = key.split('_')[1]
                menu_item = MenuItem.objects.get(pk=item_id)
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=int(value)
                )
        return super().form_valid(form)

# мой простой класс для удаления
class DeleteView(TemplateView):
    model = None
    success_url = None

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs['pk'])
        obj.delete()
        return redirect(self.success_url)

class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customer_list')

class MenuItemDeleteView(DeleteView):
    model = MenuItem
    success_url = reverse_lazy('menu_list')

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
