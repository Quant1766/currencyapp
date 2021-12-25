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
    # exchangedate = serializers.DateField(format="%Y-%m-%d")
    exchangedate = serializers.DateField()

    class Meta:
        model = Currency
        # fields = ('r030', 'txt', 'rate', 'cc', 'exchangedate')
        fields = '__all__'


class CurrencySerializePost(serializers.ModelSerializer):
    exchangedate = serializers.DateField(required=False)
    min_exchangedate = serializers.DateField(required=False)
    max_exchangedate = serializers.DateField(required=False)

    class Meta:
        model = Currency
        fields = ('exchangedate', 'min_exchangedate', 'max_exchangedate')