# coding: utf-8

from datetime import datetime

from django.contrib.auth import get_user_model, login
from django.db import transaction
from django.db.models import Q,Count, F
from django.shortcuts import redirect
from django.utils import timezone
from django.core.paginator import Paginator
from ipaddress import ip_address

from rest_framework import mixins, viewsets, status, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from engage.operator.models import RedeemPackage

from engage.core.models import HTML5Game

from .constants import (
    FriendStatus,
    SectionLog,
    SubscriptionPlan,
    Transaction
)
from engage.core.constants import WinAction, NotificationTemplate
from engage.core.models import Notifications, BattlePassMission, BattlePass,Avatar
from engage.mixins import PaginationMixin
from . import serializers
from .models import (
    FriendList,
    User,
    UserNotification,
    UserBattlePassMission,
    UserFavoriteFriend,
    SendCoinsHistory,
    UserGamePlayed,
    UserBattlePass,
    UserSectionLog,
    UserTransactionHistory
)
from .serializers import EditProfileSerializer
from ..core.serializers import TrophySerializer, StickerSerializer
from ..services import notify_when
from ..tournament.models import Tournament, TournamentPrize
from ..tournament.serializers import TournamentSerializer


UserModel = get_user_model()



class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = None
    permission_classes = (permissions.AllowAny,)

    @action(methods=['POST'], detail=False)
    def verify_mobile(self, request):
        username = request.data.get('phone_number')
      
        try:
            # user = UserModel.objects.get(
            #     username__iexact=username,
            #     region=request.region
            # )
            user = UserModel.objects.filter(
                username__iexact=username,
                region=request.region,
                is_superuser=False,
                is_staff=False
            ).first()
            if not user :
                user = UserModel.objects.filter(
                mobile__iexact=username,
                region=request.region,
                is_superuser=False,
                is_staff=False
                )
                if not user :
                   raise exceptions.ValidationError('Invalid Mobile Number')
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError('Invalid Mobile Number')

        return Response({}, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def reg_verify_mobile(self, request):
        username = request.data.get('phone_number')
        subscription = request.data.get('subscription')
      
        try:
            user = UserModel.objects.filter(
                username__iexact=username,
                region=request.region
            )
            if user:
                return Response({}, status=status.HTTP_306_RESERVED)
                
            user = UserModel.objects.filter(
                mobile__iexact=username,
                region=request.region
            )
            if user:
                return Response({}, status=status.HTTP_306_RESERVED)
        except UserModel.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)


        return Response({}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        username = request.POST.get('mobile')
        otp = request.POST.get('code')
        try:
            user = UserModel.objects.filter(
                username__iexact=username,
                region=request.region,
                is_superuser=False,
                is_staff=False
            )
            if not user :
                user = UserModel.objects.filter(
                        mobile__iexact=username,
                        region=request.region,
                        is_superuser=False,
                        is_staff=False
                        ).first()
                if not user :
                    raise exceptions.ValidationError('Invalid Mobile Number')  
                else :
                    user = UserModel.objects.get(
                        mobile__iexact=username,
                        region=request.region,
                        is_superuser=False,
                        is_staff=False
                        )         
            else :
                user = UserModel.objects.get(
                    username__iexact=username,
                    region=request.region,
                    is_superuser=False,
                    is_staff=False
                    )
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError('Invalid Mobile Number')

        @notify_when(events=[NotificationTemplate.LOGIN],
                     is_route=False, is_one_time=False)
        def notify(user, user_notifications):
            """ extra logic if needed """
        notify(user=user)

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('/')
    
    @action(methods=['POST'], detail=False)
    def register(self, request):
        username = request.POST.get('phone_number')
        subscription = request.POST.get('subscription')
        otp = request.POST.get('code')
        avatar = Avatar.objects.order_by('?').first()
        user =  User.objects.create(
                is_superuser=False,
                first_name='',
                last_name='',
                email='',
                is_active=True,
                is_staff=False,
                mobile = username,
                subscription=subscription,
                date_joined=datetime.now(),
                modified = datetime.now(),
                newsletter_subscription=True,
                timezone= '',
                country=request.region.code,
                region_id=request.region.id,
                is_billed = False,
                password='pbkdf2_sha256$260000$aMwTW2Wr3K2J2WmodFFd5W$pZUAfNohO77wQbo4oRgMYybD8Vph9HdUSoeWOHkwT9w='
            )
        user.username= 'player'+str(user.id)
        user.nickname= 'player'+str(user.id)
        
        if avatar :
            user.avatar = avatar

        user.save()

        @notify_when(events=[NotificationTemplate.LOGIN],
                     is_route=False, is_one_time=False)
        def notify(user, user_notifications):
            """ extra logic if needed """
        notify(user=user)

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('/')

class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'uid'
    search_fields = ('nickname',)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(region=self.request.region)
        if self.action == 'send_coins':
            if user.is_authenticated:
                return queryset.exclude(id=user.id)
        return queryset.filter(region=self.request.region)

    def get_serializer_class(self):
        if self.action == 'send_coins':
            return serializers.SendCoinsSerializer
        elif self.action == 'last_played_games':
            return serializers.UserGamePlayedSerializer
        elif self.action == 'joined_tournaments':
            return TournamentSerializer
        elif self.action == 'upcoming_tournaments':
            return TournamentSerializer
        elif self.action == 'previous_tournaments':
            return TournamentSerializer
        elif self.action == 'trophies':
            return TrophySerializer
        elif self.action == 'stickers':
            return StickerSerializer
        elif self.action == 'profile':
            return EditProfileSerializer   
        elif self.action == 'friends':
            return serializers.FriendSerializer
        elif self.action == 'update_user_substatus':
            return serializers.UpdateSubscriptionSerializer
        return serializers.UserSerializer

    @action(['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def unlock_battlepass_vip(self, request, uid):
        battlepass = BattlePass.objects.get_active().first()
        if not battlepass:
            raise exceptions.APIException('No active battle pass found')

        user_bp, created = UserBattlePass.objects.get_or_create(
            user=request.user,
            battlepass=battlepass,
            defaults={
                'is_vip': True,
                'vip_date': timezone.now()
            }
        )
        if not created and user_bp.is_vip:
            raise exceptions.ValidationError("User has already unlocked vip")
        else:
            user_bp.is_vip = True
            user_bp.vip_date = timezone.now()
            user_bp.save()

        return Response()
    
    @action(['POST'], detail=False)  # , permission_classes=[permissions.IsAuthenticated]
    def update_user_substatus(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msisdn = serializer.validated_data['msisdn']
        try:
            refid = serializer.validated_data['refid']
        except:
            pass
        new_substatus = serializer.validated_data['new_substatus']
        
        
        print(request.META.get('HTTP_X_FORWARDED_FOR'))
        ip = ip_address(request.META.get('HTTP_X_FORWARDED_FOR').split(",")[0])
        if not ip.is_private:
            raise exceptions.PermissionDenied('Request not Allowed!')
        userexist = User.objects.filter(mobile=msisdn)
        if not userexist:
            raise exceptions.ValidationError({'msisdn':'No user with the provided phone number was found!'})
        elif userexist.first().subscription==new_substatus:
            raise exceptions.ValidationError({'msisdn': 'User already has subscription '+ new_substatus})
        elif new_substatus not in SubscriptionPlan.values:
            raise exceptions.ValidationError({'new_substatus':'The subscription plan provided is not valid!'})
        else:
            if refid and refid != "":
                refexist = User.objects.filter(id=refid)
                if not refexist:
                    raise exceptions.ValidationError({'refid':'No referring user with the provided id was found!'})
            num = userexist.update(subscription=new_substatus)
        if num >0:
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.APIException("Error in updating user subscription!")

        

    @action(['GET'], detail=True)
    def friends(self, request, uid):
        queryset = self.get_queryset()

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        instance = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, instance)

        search = request.query_params.get('search')

        if search:
            queryset = instance.friends.filter(
                (~Q(friend=instance) & Q(friend__nickname__icontains=search)) |
                (~Q(user=instance) & Q(user__nickname__icontains=search))
            ).all()
        else:
            queryset = instance.friends.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request, 'user': instance})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={'request': request, 'user': instance})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['PUT'], detail=False, permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic()
    def profile(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_complete_profile = user.is_complete_profile

        if serializer.validated_data.get('avatar'):
            user.avatar = serializer.validated_data['avatar']
        user.nickname = serializer.validated_data['name']
        user.email = serializer.validated_data['email']
        user.country = serializer.validated_data['country']
        user.save()

        user.profile.gender = serializer.validated_data['gender']
        user.profile.birthdate = serializer.validated_data['birthdate']
        user.profile.residency = serializer.validated_data['residency']
        user.profile.save()

        # if not is_complete_profile:
        #     @notify_when(events=[NotificationTemplate.COMPLETE_PROFILE],
        #                  is_route=False, is_one_time=True)
        #     def notify(user, user_notifications):
        #         """ extra logic if needed """
        #     notify(user=user)

        return Response(status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def last_played_games(self, request, uid):
        instance = self.get_object()
        size = request.query_params.get('size')

        played_games = UserGamePlayed.objects.filter(
            user=instance,
            game__regions__in=[self.request.region]
        ).order_by('-last_played_at')
        if size:
            played_games = played_games[:int(size)]

        serializer = self.get_serializer(
            instance=played_games, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def joined_tournaments(self, request, uid):
        instance = self.get_object()
        size = request.query_params.get('size')

        tournaments = Tournament.objects.filter(
            tournamentparticipant__participant=instance,
            tournamentparticipant__is_waiting_list = False
        ).all()
        if size:
            tournaments = tournaments[:int(size)]

        serializer = self.get_serializer(instance=tournaments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def upcoming_tournaments(self, request, uid):
        instance = self.get_object()
        size = request.query_params.get('size')

        now = timezone.now()

        # tournaments = Tournament.objects.filter(
        #     tournamentparticipant__participant=instance,
        #     start_date__gt=now
        # ).all()
        tournaments = Tournament.objects.filter(
            tournamentparticipant__participant=instance,
            end_date__gt=now,
            tournamentparticipant__is_waiting_list = False
        ).all()
    
        if size:
            tournaments = tournaments[:int(size)]

        serializer = self.get_serializer(instance=tournaments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def previous_tournaments(self, request, uid):
        instance = self.get_object()
        size = request.query_params.get('size')

        now = timezone.now()
        tournaments = Tournament.objects.filter(
            tournamentparticipant__participant=instance,
            end_date__lte=now
        ).all()
        if size:
            tournaments = tournaments[:int(size)]
        serializer = self.get_serializer(instance=tournaments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def stickers(self, request, uid):
        size = request.query_params.get('size')
        instance = self.get_object()
        if size:
            query = instance.stickers.all()[:int(size)]
        else:
            query = instance.stickers.all()
        serializer = self.get_serializer(instance=query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def trophies(self, request, uid):
        size = request.query_params.get('size')
        instance = self.get_object()
        if size:
            query = instance.trophies.all()[:int(size)]
        else:
            query = instance.trophies.all()
        serializer = self.get_serializer(instance=query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(['GET'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def sections_log(self, request, uid):
        user = request.user
        new_tournament = None
        new_game = None
        new_prize = None
        new_redeem = None
        new_winner = None
        tournament_exist = UserSectionLog.objects.filter(user=user,
                                                         section_name=SectionLog.TOURNAMENT).first() 
        if tournament_exist :
            new_tournament = Tournament.objects.filter(created__gt=tournament_exist.created,regions__in=[self.request.region]).first()                                                  
             
        game_exist = UserSectionLog.objects.filter(user=user,
                                                   section_name=SectionLog.GAME).first() 
        if game_exist :
            new_game = HTML5Game.objects.filter(created__gt=game_exist.created,regions__in=[self.request.region]).first()  

        prize_exist =  UserSectionLog.objects.filter(user=user,section_name=SectionLog.PRIZE).first()
        if prize_exist :
            new_prize = TournamentPrize.objects.select_related('tournament').exclude(image='').filter(
                                                                tournament__regions__in=[self.request.region],
                                                                created__gt=prize_exist.created).first() 
        
        redeem_exist =  UserSectionLog.objects.filter(user=user,section_name=SectionLog.REDEEM).first()
        if redeem_exist :
             new_redeem = RedeemPackage.objects.filter(operator__region=request.region,created__gt=redeem_exist.created).first()

        winners_exist = UserSectionLog.objects.filter(user=user,section_name=SectionLog.WINNERS).first()
        if winners_exist :
            new_winner = TournamentPrize.objects.filter(
                winner__isnull=False,
                tournament__regions__in=[request.region],
                created__gt=winners_exist.created
            ).values('winner').annotate(
                winner_name=F('winner__nickname'),
                win_count=Count('winner')
            ).values('winner_name').order_by('-win_count').first() 

        return Response({
            'newTournamentExist':(True if new_tournament or not tournament_exist else False),
            'newPriceExist':(True if new_prize or not prize_exist else False),
            'newGameExist':(True if new_game or not game_exist else False),
            'newRedeemExist':(True if new_redeem or not redeem_exist else False),
            'newWinnerExist':(True if new_winner or not winners_exist else False)}, status=status.HTTP_200_OK)

    @action(['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def update_log(self, request,uid):
        user = request.user
        section = request.data.get('section_name')

        user_section_log, created = UserSectionLog.objects.get_or_create(user=user,
                                    section_name=section)                            
        if not created :
            user_section_log.created = timezone.now()
            user_section_log.save()                                             
        return Response(status=status.HTTP_200_OK)
    
    @action(['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def check_usercoin(self, request,uid):
        redFlag  = False
        new_user = User.objects.get(uid=uid)
        coins = new_user.coins
        old_coins = new_user.old_coins
        if new_user.seen_coins != True :
            new_user.seen_coins = True
            new_user.old_coins =  old_coins
            new_user.save()     
            redFlag = True                                        
        return Response({'redFlag':redFlag},status=status.HTTP_200_OK)
    

    @action(['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def remove_friend(self, request, uid):
        instance = self.get_object()

        try:
            friend = FriendList.objects.get(
                (Q(user=request.user) & Q(friend=instance)) |
                (Q(user=instance) & Q(friend=request.user))
            )
        except FriendList.DoesNotExist:
            raise exceptions.ValidationError('User is not on your friends list')

        if request.user == friend.user:
            other = friend.friend
        else:
            other = friend.user

        friend.delete()

        # notify the other user when friend request removed
        @notify_when(
            events=[NotificationTemplate.FRIEND_REMOVE],
            is_route=False, is_one_time=False,
            extra={
                "nickname": request.user.nickname,
                "friend": other.nickname
            }
        )
        def notify(user, user_notifications):
            """ extra logic if needed """

        notify(request.user)

        return Response(status=status.HTTP_200_OK)

    @action(['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def upgrade_subscription(self, request, uid):
        user = request.user
        if user.subscription == SubscriptionPlan.FREE :
            user.subscription = SubscriptionPlan.PAID1
            @notify_when(events=[NotificationTemplate.ONWARDANDUPWARD], is_route=False, is_one_time=False)
            def notify(user, user_notifications):
                """ extra logic if needed """
            notify(user=user)  
        else :  
            user.subscription = SubscriptionPlan.PAID2   
        user.save()


        return Response(status=status.HTTP_200_OK)


    @action(['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def add_new_friend(self, request, uid):
        instance = self.get_object()

        if request.user == instance:
            raise exceptions.ValidationError('Users cannot be friends with themselves')

        try:
            obj = FriendList.objects.get(
                (Q(user=request.user) & Q(friend=instance)) |
                (Q(user=instance) & Q(friend=request.user))
            )
        except FriendList.DoesNotExist:
            FriendList.objects.create(
                user=request.user,
                friend=instance,
                status=FriendStatus.PENDING
            )
            return Response(status=status.HTTP_200_OK)

        raise exceptions.ValidationError('User is already on your friends list')

    @action(['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic()
    def send_coins(self, request, uid):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        SendCoinsHistory.objects.create(
            user=request.user,
            receiver=instance,
            amount=serializer.validated_data['amount']
        )

        return Response(status=status.HTTP_200_OK)

    @action(['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def set_favorite(self, request, uid):
        instance = self.get_object()

        favorite_friend, created = UserFavoriteFriend.objects.get_or_create(
            user=request.user,
            friend=instance
        )

        if not created:
            is_favorite = False
            favorite_friend.delete()
        else:
            is_favorite = True

        return Response({'is_favorite': is_favorite}, status=status.HTTP_200_OK)


class FriendViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = FriendList.objects.all()
    serializer_class = serializers.FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        search = self.request.query_params.get('search')
        if search:
            queryset = user.friends.filter(
                (~Q(friend=user) & Q(friend__nickname__icontains=search)) |
                (~Q(user=user) & Q(user__nickname__icontains=search)),
            ).order_by('friend__username')
        else:
            
            queryset = user.friends.order_by('friend__username')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        if self.action == 'list':
            return {
                'user': self.request.user,
                **super().get_serializer_context()
            }
        return super().get_serializer_context()

    @action(['POST'], detail=False)
    def accept_friend_request(self, request):
        friend_uid = request.POST.get('friend', None)
        try:
            friend = UserModel.objects.filter(
                uid=friend_uid,
                region=request.region
            ).first()
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError('User not found')

        get_friend = FriendList.objects.filter(
            user=friend,
            friend=request.user,
            status=FriendStatus.PENDING
        ).first()

        if get_friend:
            get_friend.status = FriendStatus.ACCEPTED
            get_friend.save()

            get_notification = UserNotification.objects.filter(
                friend_uid=friend_uid,
                user=request.user
            ).first()
            print(get_notification)
            if get_notification: get_notification.delete()

        return Response(status=status.HTTP_200_OK)

    @action(['POST'], detail=False)
    def reject_friend_request(self, request):
        friend_uid = request.POST.get('friend', None)
        try:
            friend = UserModel.objects.filter(
                uid=friend_uid,
                region=request.region
            ).first()
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError('User not found')

        get_friend = FriendList.objects.filter(
            user=friend,
            friend=request.user,
            status=FriendStatus.PENDING
        ).first()

        if get_friend:
            get_friend.delete()

            get_notification = UserNotification.objects.filter(
                friend_uid=friend_uid,
            ).first()
            print(get_notification)
            if get_notification: get_notification.delete()

        return Response(status=status.HTTP_200_OK)


class FCMViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, PaginationMixin):
    queryset = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            return UserNotification.objects.filter(user=user).all()

    def get_serializer_class(self):
        return serializers.UserNotificationSerializer

    @action(detail=False, methods=['post'])
    def set_web_token(self, request):
        user = request.user
        fcm_token = request.data.get('fcm_token', '')

        user.web_fcm_token = fcm_token
        user.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_new_notifications(self, request):
        recent_notifications = UserNotification.objects.select_related(
            'notification'
        ).filter(
            user=request.user,
            last_read__isnull=True
        ).all().order_by('-created')
        serializer = self.get_serializer(recent_notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def get_user_notifications(self, request):
        recent_notification = UserNotification.objects.select_related(
            'notification'
        ).filter(
            user=request.user,
            last_read__isnull=True,
            notification__title=self.request.query_params.get('title'),
            notification__text=self.request.query_params.get('body'),

        ).all().order_by('-created').first()
        if recent_notification : 
            package_ids = [x.id for x in recent_notification.notification.package.all()] 
        else :
            package_ids = []    
        user=request.user
        serializer = self.get_serializer(recent_notification)
        return Response({"data":serializer.data,"subscription":user.subscription,'package_ids':package_ids})


    @action(detail=False, methods=['get'])
    def get_early_notifications(self, request):
        recent_notifications = UserNotification.objects.select_related(
            'notification'
        ).filter(
            user=request.user, last_read__isnull=False
        ).all().order_by('-created')

        page_number = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('size', 10)

        paginator = Paginator(recent_notifications, page_size)

        try:
            notifications = paginator.page(int(page_number))
        except:
            notifications = paginator.page(1)

        serializer = self.get_serializer(notifications, many=True)

        return Response({
            "data": serializer.data,
            "pagination": {
                "has_next": notifications.has_next()
            }
        })

    @action(detail=False, methods=['post'])
    def set_notification_status(self, request):
        notification_id = request.POST.get('id', None)

        try:
            notification = UserNotification.objects.get(
                user=request.user,
                id=notification_id
            )
        except UserNotification.DoesNotExist:
            return Response({'status': 'fail'}, status=status.HTTP_304_NOT_MODIFIED)

        notification.last_read = timezone.now()
        notification.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def claim_gift(self, request):
        notification_id = request.POST.get('id', None)
        try:
            notification = Notifications.objects.get(id=notification_id,
                                                     is_gift=True)
        except Notifications.DoesNotExist:
            return Response({'status': 'fail'},
                            status=status.HTTP_304_NOT_MODIFIED)

        if notification.video:
            now = datetime.now(tz=timezone.utc)

            today_battlepass = BattlePassMission.objects.filter(
                date__year=now.year,
                date__month=now.month,
                date__day=now.day,
                mission__action__in=[WinAction.WATCH_VIDEO, WinAction.WATCH_2_VIDEOS]
            ).first()

            if today_battlepass:
                if today_battlepass.mission.action == WinAction.WATCH_VIDEO:
                    obj, created = UserBattlePassMission.objects.select_related(
                        'user',
                        'bp_mission',
                        'bp_mission__mission'
                    ).get_or_create(
                        bp_mission=today_battlepass,
                        user=request.user,
                        is_completed=True
                    )
                else:
                    obj, created = UserBattlePassMission.objects.select_related(
                        'user',
                        'bp_mission',
                        'bp_mission__mission'
                    ).get_or_create(
                        bp_mission=today_battlepass,
                        user=request.user,
                    )

                    obj.count += 1

                    if not created:
                        obj.is_completed = True

                    obj.save()

        try:
            user_notification = UserNotification.objects.get(
                user=request.user,
                notification=notification_id,
                is_claimed=False
            )
        except UserNotification.DoesNotExist:
            return Response({'status': 'fail'},
                            status=status.HTTP_304_NOT_MODIFIED)

        if user_notification.notification.is_gift:
            user_notification.is_claimed = True
            user_notification.save()

            UserTransactionHistory.objects.create(
                user=request.user,
                amount=user_notification.notification.gifted_coins,
                info = Transaction.NOTIFICATION_CLAIM+' '+ user_notification.notification.title
            )

        return Response({'status': 'success','coins':request.user.coins}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_my_coins(self, request):
        return Response({
            'data': {
                'coins': request.user.coins
            },
            'status': 'success'
        }, status=status.HTTP_200_OK)
