from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_price_with_discount(value, arg):
    return int(value * arg / settings.PERCENT_TO_VALUE)
