import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from payments.models import Item, Order
from payments.utils import get_order, get_user_cart

stripe.api_key = settings.STRIPE_SECRET_KEY


class CartView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["iscart"] = True
        return context

    def get_queryset(self, *args, **kwargs):
        return get_user_cart(self.request.user)


class CreateCheckoutSessionFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        items = get_user_cart(request.user)
        if len(items) == 0:
            return redirect('payments:item_list')
        domain = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            allow_promotion_codes=True,
            payment_method_types=['card'],
            line_items=get_order(items, 'usd'),
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        domain = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=get_order((item,), item.currency),
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)

    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        domain = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=get_order((item,), item.currency),
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })
        return context


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["cart"] = get_user_cart(self.request.user)
        return context


class SuccesView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


def remove_from_cart(request, pk):
    obj = get_object_or_404(Order, user=request.user,
                            item=Item.objects.get(pk=pk)
                            )
    obj.delete()
    return redirect(reverse('payments:cart'))


def add_item_to_cart(request, pk):
    Order.objects.get_or_create(
        user=request.user, item=Item.objects.get(pk=pk)
    )
    return redirect(reverse('payments:item_list'))