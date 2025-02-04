from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=[
        ('drinks', 'Напитки'),
        ('main', 'Основные блюда'),
        ('desserts', 'Десерты'),
    ])
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('wait', 'Ожидается'),
        ('in_progress', 'В процессе'),
        ('finish', 'Завершён')
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='wait',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ {self.id} - {self.customer.name}'

    @property
    def total_price(self):
        return sum(item.menu_item.price * item.quantity for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

