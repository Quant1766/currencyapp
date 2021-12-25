from rest_framework import serializers

from Currency.models import UserModel, Currency


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password",)


class CurrencySerializer(serializers.ModelSerializer):
    exchangedate = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Currency
        fields = '__all__'


class CurrencySerializePost(serializers.ModelSerializer):
    exchangedate = serializers.DateField(format="%Y-%m-%d", required=False)
    min_exchangedate = serializers.DateField(format="%Y-%m-%d", required=False)
    max_exchangedate = serializers.DateField(format="%Y-%m-%d", required=False)

    class Meta:
        model = Currency
        fields = ('exchangedate', 'min_exchangedate', 'max_exchangedate')
