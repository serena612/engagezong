from django.db.models import Case, When, Value
from rest_framework import mixins, viewsets, status, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from engage.account.constants import Transaction, CoinTransaction

from engage.core.models import HTML5Game, Avatar, FeaturedGame
from engage.account.exceptions import CoinLimitReached
from engage.account.models import UserTransactionHistory
from . import serializers
from .constants import HTML5GameType, NotificationTemplate


class AvatarViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Avatar.objects.all()
    serializer_class = serializers.AvatarSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HTML5GameViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = HTML5Game.objects.all()
    serializer_class = serializers.HTML5GameSerializer
    permission_classes = (AllowAny,)
    search_fields = ('game',)

    def get_queryset(self):
        queryset = HTML5Game.objects.filter(regions__in=[self.request.region])

        game_type = self.request.query_params.get('game_type')
        if game_type == HTML5GameType.PREMIUM.lower():
            user = self.request.user
            if user.is_authenticated and not user.is_subscriber:
                return queryset.annotate(
                    relevancy=Case(
                        When(game_type=HTML5GameType.FREE, then=Value(1)),
                        When(game_type=HTML5GameType.EXCLUSIVE, then=Value(2)),
                        When(game_type=HTML5GameType.PREMIUM, then=Value(3)),
                    )
                ).order_by('relevancy')
            else:
                return queryset
        else:
            return queryset.filter(game_type=HTML5GameType.FREE)


class ContactViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'support':
            return serializers.ContactSupportSerializer
        else:
            return serializers.ContactEngageSerializer

    @action(methods=['POST'], detail=False)
    def support(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def engage(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class FeaturedGameViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = FeaturedGame.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        featured_game = self.queryset.get(name=instance)
        new_coins = featured_game.nbr_of_coins if  featured_game else 10
        transaction = UserTransactionHistory.objects.create(
            user=request.user,
            amount=new_coins,
            action=CoinTransaction.RETRIEVE,
            info=Transaction.RETRIEVE
        )
        print(transaction.actual_amount)
        print(transaction.__dict__)
        if transaction.actual_amount == 0:
            raise CoinLimitReached()
        else:
            return Response({'coins': new_coins})