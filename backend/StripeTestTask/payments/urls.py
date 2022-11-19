from django.urls import path

from payments.views import (CancelView, CartView,
                            CreateCheckoutSessionFromCartView,
                            CreateCheckoutSessionView, ItemDetailView,
                            ItemListView, SuccesView, add_item_to_cart,
                            remove_from_cart)

app_name = 'payments'

urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name='buy_item'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/buy/', CreateCheckoutSessionFromCartView.as_view(),
         name='buy_from_cart'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:pk>/add_to_cart/', add_item_to_cart, name='add_to_cart'),
    path('item/<int:pk>/remove_from_cart/',
         remove_from_cart, name='remove_from_cart'),
    path('success/', SuccesView.as_view(), name='success'),
]
