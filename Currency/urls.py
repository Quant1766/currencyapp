from django.urls import path, include

from Currency.api import CurrencyAPI, CreateUserView, currency_view, MyViewSet

# Inlcude the schema view in our urls.
urlpatterns = [
    path('currency/', CurrencyAPI.as_view(), name='exchange'),
    path('register/', CreateUserView.as_view(), name='register'),
    # path('sw/', MyViewSet.as_view({'get': }), name='sw'),

    path('currency_view/', currency_view, name='currency_view')
]
