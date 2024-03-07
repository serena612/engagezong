# coding: utf-8

from rest_framework import serializers

from engage.account.constants import SubscriptionPlan
from engage.account.models import UserGamePlayed
from .constants import HTML5GameType
from .models import Notifications, HTML5Game, Avatar, Trophy, Sticker, \
    FeaturedGame
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

__all__ = (
    'NotificationsSerializer',
    'TrophySerializer',
    'StickerSerializer',
    'HTML5GameSerializer'
)


class FeaturedGameSerializer(TranslatableModelSerializer): #serializers.ModelSerializer
    translations = TranslatedFieldsField(shared_model=HTML5Game)
    class Meta:
        model = FeaturedGame
        exclude = ('created', 'modified')


class NotificationsSerializer(TranslatableModelSerializer): #serializers.ModelSerializer
    translations = TranslatedFieldsField(shared_model=Notifications)
    class Meta:
        model = Notifications
        exclude = ('created', 'image',)


class HTML5GameSerializer(TranslatableModelSerializer): #serializers.ModelSerializer
    translations = TranslatedFieldsField(shared_model=HTML5Game)
    game = serializers.CharField(source='get_game_display', read_only=True)
    is_locked = serializers.SerializerMethodField()

    class Meta:
        model = HTML5Game
        fields = '__all__'

    def get_is_locked(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return True
        #obj.game_type
        if obj.game_type == HTML5GameType.FREE:
            return False
        #locked
        elif obj.game_type == HTML5GameType.EXCLUSIVE:
            return (user.subscription == SubscriptionPlan.FREE or user.is_billed == False) and \
                   UserGamePlayed.objects.filter(user=user, game=obj).exists()
        else:
            return True
        
        # elif obj.game_type == HTML5GameType.EXCLUSIVE:
        #     return (user.subscription == SubscriptionPlan.FREE or user.is_billed == False) and \
        #            UserGamePlayed.objects.filter(user=user, game=obj).exists()
        # else:
        #     return (user.subscription == SubscriptionPlan.FREE or user.is_billed == False)


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        exclude = ('configuration',)


class ContactEngageSerializer(serializers.Serializer):
    name = serializers.CharField()  # min_length=3
    phone_number = serializers.CharField()
    country = serializers.CharField()
    email = serializers.EmailField()
    company = serializers.CharField(required=False, allow_blank=True,
                                    allow_null=True)
    message = serializers.CharField(allow_blank=False)


class ContactSupportSerializer(serializers.Serializer):
    username = serializers.CharField()  # min_length=3
    phone_number = serializers.CharField()
    country = serializers.CharField()
    email = serializers.EmailField()
    support_type = serializers.CharField()
    message = serializers.CharField(allow_blank=False)


class TrophySerializer(serializers.ModelSerializer):

    class Meta:
        model = Trophy
        fields = '__all__'


class StickerSerializer(TranslatableModelSerializer): #serializers.ModelSerializer
    translations = TranslatedFieldsField(shared_model=Sticker)
    class Meta:
        model = Sticker
        fields = '__all__'