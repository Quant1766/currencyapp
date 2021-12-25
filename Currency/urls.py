from django.urls import path

from Currency.api import CurrencyAPI, CreateUserView

# Inlcude the schema view in our urls.
urlpatterns = [
    path('currency/', CurrencyAPI.as_view(), name='exchange'),
    path('register/', CreateUserView.as_view(), name='register'),

]
