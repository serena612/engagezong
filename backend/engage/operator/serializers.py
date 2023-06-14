from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError, APIException

from .models import Region, Operator, RedeemPackage, PurchaseCoin, OperatorAd, SubConfiguration
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField


class NotEnoughCoinsException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    # default_detail = 'You don\'t have enough coins in your wallet to redeem this prize. Purchase some coins?'
    default_detail = 'You don\'t have enough coins in your wallet to redeem this prize.'
    default_code = 'low_coins'


class RegionSerializer(serializers.ModelSerializer): #serializers.ModelSerializer

    class Meta:
        model = Region
        fields = '__all__'


class OperatorSerializer(TranslatableModelSerializer): #serializers.ModelSerializer
    translations = TranslatedFieldsField(shared_model=Operator)
    class Meta:
        model = Operator
        fields = '__all__'


class RedeemPackageSerializer(TranslatableModelSerializer): #serializers.Serializer
    translations = TranslatedFieldsField(shared_model=RedeemPackage)
    package = serializers.PrimaryKeyRelatedField(
        queryset=RedeemPackage.objects.all(),
        required=True
    )

    def validate_package(self, obj):
        user = self.context['request'].user

        if obj.coins > user.coins:
            raise NotEnoughCoinsException()

        return obj


class PurchaseCoinsSerializer(serializers.Serializer):
    coins_plan = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseCoin.objects.all(),
        required=True
    )

class SubConfigurationSerializer(serializers.Serializer):
    is_sub = serializers.PrimaryKeyRelatedField(
        queryset=SubConfiguration.objects.all(),
        required=True
    )
