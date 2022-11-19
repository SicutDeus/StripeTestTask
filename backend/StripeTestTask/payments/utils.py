from django.conf import settings

from payments.models import Item, Order


def get_user_cart(user):
    orders = Order.objects.filter(user=user)
    items = Item.objects.none()
    for order in orders:
        items |= Item.objects.filter(pk=order.item.pk)
    return items


def get_order(items, currency):
    order_list = list()
    for item in items:
        if item.currency == 'rub' and currency == 'usd':
            price = int(item.price * 100 * settings.RUB_TO_USD)
        else:
            price = int(item.price) * 100
        order_list.append(
            {
                'price_data': {
                    'currency': currency,
                    'unit_amount': price,
                    'product_data': {
                        'name': item.name,
                    },
                },
                'quantity': 1,
            },
        )
    return order_list
