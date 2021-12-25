from datetime import datetime

import django_filters

from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from Currency.serializers import UserSerializer, CurrencySerializer, Currency, CurrencySerializePost
from rest_framework.response import Response


from rest_framework.schemas.openapi import AutoSchema

class SimpleFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        foo = request.query_params.get("foo")
        if foo:
            queryset = queryset.filter(foo=foo)
        return queryset

    def get_schema_operation_parameters(self, view):
        return [{
            "name": "foo",
            "in": "query",
            "required": True,
            "description": "What foo does...",
            "schema": {"type": "string"}
        }]

class MyViewSet(ModelViewSet):
    filter_backends = [SimpleFilterBackend]

class CustomSchema(AutoSchema):
    def get_operation(self, path, method):
        op = super().get_operation(path, method)
        op['parameters'].append({
            "name": "foo",
            "in": "query",
            "required": True,
            "description": "What foo does...",
            'schema': {'type': 'string'}
        })
        return op


# class MyViewSet(ModelViewSet):
#     schema = CustomSchema()
#
#     def get_queryset(self):
#         foo = self.request.query_params.get("foo")
#         if foo:
#             self.queryset = self.queryset.filter(foo=foo)
#         return self.queryset


class CurrencyFilter(django_filters.FilterSet):
    min_exchangedate = django_filters.NumberFilter(name="exchangedate", lookup_type='gte')
    max_exchangedate = django_filters.NumberFilter(name="exchangedate", lookup_type='lte')

    class Meta:
        model = Currency
        fields = ['min_exchangedate', 'max_exchangedate', 'exchangedate']


@api_view(['POST'])
def currency_view(request):
    """
    Your docs
    ---
    # YAML (must be separated by `---`)

    type:
      name:
        required: true
        type: string
      url:
        required: false
        type: url
      created_at:
        required: true
        type: string
        format: date-time

    serializer: .serializers.FooSerializer
    omit_serializer: false

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: name
          description: Foobar long description goes here
          required: true
          type: string
          paramType: form
        - name: other_foo
          paramType: query
        - name: other_bar
          paramType: query
        - name: avatar
          type: file

    responseMessages:
        - code: 401
          message: Not authenticated
    """


    from_date = request.data.get('min_exchangedate', None)
    to_date = request.data.get('max_exchangedate', None)
    date_c = request.data.get('exchangedate', None)
    if date_c:
        queryset = Currency.objects.filter(
            exchangedate=datetime.strptime(date_c, '%Y-%m-%d'),
        )
    elif to_date and from_date:
        queryset = Currency.objects.filter(
            exchangedate__gte=datetime.strptime(from_date, '%Y-%m-%d'),
            exchangedate__lte=datetime.strptime(to_date, '%Y-%m-%d')
        )
    elif to_date:
        from_date = '06.01.1996'  # date of first record
        queryset = Currency.objects.filter(
            exchangedate__gte=datetime.strptime(from_date, '%Y-%m-%d'),
            exchangedate__lte=datetime.strptime(to_date, '%Y-%m-%d')
        )

    elif from_date:
        queryset = Currency.objects.filter(
            exchangedate__gte=datetime.strptime(from_date, '%Y-%m-%d'),
            exchangedate__lte=datetime.now().date()
        )
    else:
        queryset = Currency.objects.filter(
            exchangedate=datetime.now().date(),
        )

    serializer = CurrencySerializer(queryset, many=True)
    print('queryset', queryset.values('exchangedate'))
    print('serializer', serializer)

    return Response(serializer.data)

class CurrencyAPI(ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencySerializePost
    model = Currency

    # filter_class = CurrencyFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CurrencySerializer(queryset, many=True)
        print('queryset', queryset.values('exchangedate'))
        print('serializer', serializer)

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
