from datetime import datetime

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model

from Currency.serializers import UserSerializer, CurrencySerializer, Currency, CurrencySerializePost
from rest_framework.response import Response


class CurrencyAPI(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencySerializePost
    model = Currency
    http_method_names = ['post']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CurrencySerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        from_date = self.request.data.get('min_exchangedate', None)
        to_date = self.request.data.get('max_exchangedate', None)
        date_c = self.request.data.get('exchangedate', None)
        if date_c:
            queryset = self.model.objects.filter(
                exchangedate=datetime.strptime(date_c, '%Y-%m-%d'),
            )
        elif to_date and from_date:
            queryset = self.model.objects.filter(
                exchangedate__gte=datetime.strptime(from_date, '%Y-%m-%d'),
                exchangedate__lte=datetime.strptime(to_date, '%Y-%m-%d')
            )
        elif to_date:
            from_date = '06.01.1996'  # date of first record
            queryset = self.model.objects.filter(
                exchangedate__gte=datetime.strptime(from_date, '%Y-%m-%d'),
                exchangedate__lte=datetime.strptime(to_date, '%Y-%m-%d')
            )

        elif from_date:
            queryset = self.model.objects.filter(
                exchangedate__gte=datetime.strptime(from_date, '%Y-%m-%d'),
                exchangedate__lte=datetime.now().date()
            )
        else:
            queryset = self.model.objects.filter(
                exchangedate=datetime.now().date(),
            )
        return queryset


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = UserSerializer
