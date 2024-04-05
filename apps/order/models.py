from django.db import models


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
        # unique_together = ('user', 'product' ) # Щоб не можна було додати один і той же товар в корзину більше одного разу


class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Користувач')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        verbose_name = 'Обране'
        verbose_name_plural = 'Обране'
        unique_together = ('user', 'product' ) # Щоб не можна було додати один і той же товар в обране більше одного разу