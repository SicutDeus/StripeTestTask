from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Currencies(models.TextChoices):
    USD = 'usd'
    RUB = 'rub'


class Item(models.Model):
    name = models.CharField(
        'название предмета',
        max_length=255,
        help_text='Введите название предмета',
    )
    description = models.TextField(
        'описание предмета',
        help_text='Введите описание предмета',
    )
    price = models.IntegerField(
        'стоимость предмета',
        help_text='Введите стоимость предмета',
    )
    currency = models.CharField(
        'валюта',
        help_text='Выберите валюту',
        max_length=3,
        choices=Currencies.choices,
        default=Currencies.USD,
    )

    class Meta:
        ordering = ('price',)
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", args=(self.pk,))


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='товар из корзины',
    )

    def __str__(self) -> str:
        return f'Корзина {self.user.username}'

    class Meta:
        default_related_name = 'order'
