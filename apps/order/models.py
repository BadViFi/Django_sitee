from django.db import models


from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Користувач')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Кількість')

    def __str__(self):
        return f'{self.product.name} - {self.quantity} шт.'

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'
        ordering = ('id',)
        # unique_together = ('user', 'product' ) # Щоб не можна було додати один і той же товар в корзину більше одного разу
    
    def total_price(self):
        return self.product.price * self.quantity


class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Користувач')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        verbose_name = 'Обране'
        verbose_name_plural = 'Обране'
        unique_together = ('user', 'product' ) # Щоб не можна було додати один і той же товар в обране більше одного разу



class Order(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'В обробці'),
        ('sent', 'Відправлено'),
        ('completed', 'Завершено'),
        ('canceled', 'Скасовано')
    )
    STATUS_PAID = (
        (True, 'Оплачено'),
        (False, 'Не оплачено')
    )

    discount_applied = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Користувач')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Загальна вартість')

    first_name = models.CharField(max_length=255, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = PhoneNumberField(verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адреса')
    comment = models.TextField(verbose_name='Коментар', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    paid = models.BooleanField(verbose_name='Оплачено', choices=STATUS_PAID, default=False)
    status = models.CharField(max_length=255, verbose_name='Статус', choices=STATUS_CHOICES, default='in_progress')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Замовлення №{self.id}'



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Замовлення')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Кількість')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')

    def __str__(self):
        return f'{self.product.name} - {self.quantity} шт.'

    class Meta:
        verbose_name = 'Товар замовлення'
        verbose_name_plural = 'Товари замовлення'

    def total_price(self):
        return self.product.price * self.quantity