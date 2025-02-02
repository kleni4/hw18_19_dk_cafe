from django import forms
from django.core.validators import RegexValidator
from .models import Customer, MenuItem, Order, OrderItem

# https://docs.djangoproject.com/en/5.1/ref/validators/
class CustomerForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+7XXXXXXXXXX'. До 15 цифр разрешено."
    )
    
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text='Формат: +7XXXXXXXXXX',
        widget=forms.TextInput(attrs={
            'placeholder': '+7XXXXXXXXXX',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        # Удаляем все нецифровые символы
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        
       
        if len(cleaned_phone) != 11:
            raise forms.ValidationError('Номер телефона должен содержать 11 цифр')
        
        return cleaned_phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'available']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля')
        return price

    def clean_name(self):
        name = self.cleaned_data['name']
        if MenuItem.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Блюдо с таким названием уже существует')
        return name

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        
        # Проверяем, что заказ не может быть завершен, если он новый
        if status == 'finish' and self.instance.pk is None:
            raise forms.ValidationError('Новый заказ не может быть сразу завершён')
            
        return cleaned_data

    def clean_customer(self):
        customer = self.cleaned_data['customer']
        if not customer.id:
            raise forms.ValidationError('Выберите существующего клиента')
        return customer

class OrderItemForm(forms.ModelForm):
    menu_item = forms.ModelChoiceField(
        queryset=MenuItem.objects.all(),
        empty_label="Выберите блюдо",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'})
    )

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError('Количество должно быть больше нуля')
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        menu_item = cleaned_data.get('menu_item')
        
        if menu_item and not menu_item.available:
            raise forms.ValidationError('Это блюдо недоступно для заказа')
            
        return cleaned_data
