import django_filters
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Count, F, Q, Prefetch, Case, When
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import mixins, viewsets, status, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import Value
from engage.account.models import User
from engage.services import notify_when
from engage.core.constants import NotificationTemplate

from engage.account.exceptions import (
    GameAccountUnavailable,
    MinimumProfileLevelException
)
from .constants import TournamentState
from .exceptions import ParticipantExists, FreeUserCannotJoinTournament,TournamentCloseException,TournamentFirstException,TournamentStartException
from .models import (
    Tournament,
    TournamentParticipant,
    TournamentPrize,
    TournamentMatch
)
from .serializers import (
    TournamentSerializer,
    TournamentParticipantSerializer,
    TournamentPrizeSerializer,
    TournamentWinnerSerializer
)
from ..core.models import Sticker
from ..operator.constants import SubscriptionType


class TournamentFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(choices=TournamentState.choices,
                                        method='filter_state')

    def filter_state(self, queryset, name, value):

        if value == TournamentState.UPCOMING:
            return queryset.upcoming()
        elif value == TournamentState.PAST:
            return queryset.past()
        elif value == TournamentState.ONGOING:
            return queryset.ongoing()

    class Meta:
        model = Tournament
        fields = ('state',)


class TournamentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Tournament.objects.select_related('game').prefetch_related(
        'tournamentparticipant_set',
        Prefetch(
            'tournamentprize_set',
            queryset=TournamentPrize.objects.order_by('position')
        )
    )
    serializer_class = TournamentSerializer
    permission_classes = (permissions.AllowAny,)
    search_fields = ('name',)
    ordering_fields = ['created', 'start_date']
    lookup_field = 'slug'


    # def get_queryset(self):
    #     user = self.request.user
    #     now = timezone.now()
    #     queryset = self.queryset.filter(regions__in=[self.request.region])

    #     if self.action in ['start', 'join']:
    #         return queryset.all()

    #     state = self.request.query_params.get('state', TournamentState.UPCOMING)
        
    #           # if user.is_authenticated :
    #         # queryset = queryset.filter(Q(open_date__lte=now) |
    #         #                            Q(Q(minimum_profile_level__lte=user.level) | Q(minimum_profile_level__isnull=True))
                                       
    #         # ).order_by('open_date')
        
    #     if not user.is_authenticated:
    #         queryset = queryset.filter(
    #             free_open_date__lte=now,
    #         ).order_by('free_open_date')
            
    #     # if not user.is_subscriber:
    #     else :
    #         queryset = queryset.annotate(
    #             is_min_level=Case(
    #                 When(Q(minimum_profile_level__isnull=False) &
    #                      Q(minimum_profile_level__gt=user.level),
    #                      then=False),
    #                 default=True
    #             )
    #         ).filter(
    #              Q(free_open_date__lte=now) |
    #             (Q(Q(minimum_profile_level__lte=user.level) | Q(minimum_profile_level__isnull=True)) & Q(free_open_date__gt=now))
    #         ).order_by('free_open_date')

    #     if self.action == 'list':
    #         if state == TournamentState.UPCOMING:
    #             return queryset.filter(end_date__gte=now)
    #         else:
    #             return queryset.filter(end_date__lt=now)
    #     else:
    #         return queryset.all()

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        queryset = self.queryset.filter(regions__in=[self.request.region])
       

        if self.action in ['start', 'join', 'close']:
            return queryset.all()

        state = self.request.query_params.get('state', TournamentState.UPCOMING)
        game = self.request.query_params.get('game', 0)
        if game != '0' :
            queryset = queryset.filter(game__id=int(game))
        
        # if user.is_authenticated :
            # queryset = queryset.filter(Q(open_date__lte=now) |
            #                            Q(Q(minimum_profile_level__lte=user.level) | Q(minimum_profile_level__isnull=True))
                                       
            # ).order_by('open_date')
        
        if not user.is_authenticated:
            queryset = queryset.filter(
                free_open_date__lte=now,
            ).order_by('free_open_date')
            
        else :
            queryset = queryset.annotate(
                is_min_level=Case(
                    When(Q(minimum_profile_level__isnull=False) &
                         Q(minimum_profile_level__gt=user.level),
                         then=False),
                    default=True
                )
            ).filter(
                 Q(free_open_date__lte=now) |
                (Q(Q(minimum_profile_level__lte=user.level) | Q(minimum_profile_level__isnull=True)) & Q(free_open_date__gt=now))
            ).order_by('free_open_date')
        

        if self.action == 'list':
            if state == TournamentState.UPCOMING:
                tournaments = queryset.filter(end_date__gte=now,started_on__isnull=True)
            elif state == TournamentState.PAST:
                tournaments =  queryset.filter(end_date__lt=now)
            elif state == TournamentState.ONGOING:
                tournaments = queryset.filter(end_date__gt=now,started_on__isnull=False)
            else:
                tournaments =  queryset.all() 
        else:
            tournaments =  queryset.all() 
       
        return  tournaments  

            

    @action(methods=['GET'], detail=True, permission_classes=(permissions.IsAdminUser,))
    @transaction.atomic()
    def start(self, request, slug):
        tournament = self.get_object()
        
        
        if tournament.started_on:
            raise TournamentStartException() 

        room_size = tournament.game.room_size
        participants = tournament.tournamentparticipant_set.all()
        count = participants.count()

        if not count:
            raise TournamentFirstException()
           
        if not room_size:
            return redirect(request.META["HTTP_REFERER"])

        # for k, i in enumerate(range(0, count, room_size), 1):
        #     TournamentMatch.objects.create( 
        #         tournament=tournament,
        #         match_name=f'[Round 1] Match {k}',
        #         round_number=1,
        #     )

        tournament.started_on = timezone.now()
        tournament.save()

        return redirect(request.META["HTTP_REFERER"])
    

    @action(methods=['GET'], detail=True, permission_classes=(permissions.IsAdminUser,))
    @transaction.atomic()
    def close(self, request, slug):
        tournament = self.get_object()
        

        prizes = tournament.tournamentprize_set.filter(winner__isnull=True)
        count = prizes.count()

        if count :
            raise TournamentCloseException()


        tournament.end_date = timezone.now()
        tournament.closed_on = timezone.now()
        tournament.save()
        tournament.send_notification_close()
        # tournament_prizes = TournamentPrize.objects.filter(
        # tournament__id=tournament.id
        #  )
        # tournament_winners= tournament_prizes.values_list('winner', flat=True)
        # failed_participants_ids = TournamentParticipant.objects.filter(
        #     tournament__id=tournament.id,
        # ).exclude(participant__id__in=tournament_winners).values_list('participant', flat=True)
        # failed_participants = User.objects.filter(id__in=failed_participants_ids)

        # # print(failed_participants)
        # for prize in tournament_prizes :
        #     # USER_FIRST_TOURNAMENT

        #     if prize.position == 1 :
        #         @notify_when(events=[NotificationTemplate.USER_FIRST_TOURNAMENT], is_route=False, is_one_time=False)
        #         def notify(user, user_notifications):
        #             """ extra logic if needed """
        #             for notificationi in user_notifications:
        #                 notificationi.link=self.name+";"+prize.title+";"+str(prize.image)
        #                 notificationi.save()
        #         notify(prize.winner)

        # # USER_SECOND_THIRD_TOURNAMENT >> Users who are second, third or positions that win a prize.
        #     elif  prize.position >= 2 :

        #         @notify_when(events=[NotificationTemplate.USER_SECOND_THIRD_TOURNAMENT], is_route=False, is_one_time=False)
        #         def notify(user, user_notifications):
        #             """ extra logic if needed """
        #             for notificationi in user_notifications:
        #                 notificationi.link=self.name+";"+prize.title+";"+str(prize.image)
        #                 notificationi.save()
        #         notify(prize.winner)
 
        # print("failed participants", failed_participants)
        # if failed_participants :
        #     for participant in  failed_participants :
        #         print("processing sticker for", participant)
        #         sticker = Sticker.objects.filter(  # .select_for_update()
        #                     ~Q(id__in=participant.stickers.all())
        #                 ).order_by('?').first()
        #         print("sticker", sticker)
        #         print("tourn giff", tournament.give_sticker)
        #         if tournament.give_sticker:
        #             if sticker :
                        
        #                 participant.stickers.add(sticker)
        #                 #participant.refresh_from_db()
        #                 participant.save()
        #                 print("participantid", participant.id)
        #                 print("stickerid", sticker.id)
        #                 print("sticker added !")
        #                 print("stickers after save", participant.stickers.all())
        #         print("coins per participant", tournament.coins_per_participant)
        #         print("weird condition", participant.stickers.all())
        #         if tournament.coins_per_participant > 0 :
        #             if participant.stickers.all() :
        #                 participant.old_coins = participant.coins
        #                 print("adding", tournament.coins_per_participant, "coins to", participant.coins)
        #                 participant.coins = participant.coins + tournament.coins_per_participant
        #                 participant.seen_coins = False
        #                 participant.save()            
            
        #         @notify_when(events=[NotificationTemplate.USER_OUTSIDE_THE_WINNING_POSITIONS], is_route=False, is_one_time=False)
        #         def notify(user, user_notifications):
        #             """ extra logic if needed """
        #             for notificationi in user_notifications:
        #                 notificationi.link=("1" if tournament.give_sticker else "0")+";"+(str(tournament.coins_per_participant) if tournament.coins_per_participant else "0")+";"+(str(sticker.image) if tournament.give_sticker and sticker and sticker.image  else "-")
        #                 notificationi.save()
        #                 # print(notificationi.link)
        #         notify(participant)
        return redirect(request.META["HTTP_REFERER"])


    @action(methods=['POST'], detail=True, permission_classes=(permissions.IsAuthenticated,))
    def join(self, request, slug):
        now = timezone.now()
        tournament = self.get_object()
        user = request.user
        linked_account = user.usergamelinkedaccount_set.filter(
            game=tournament.game
        ).first()
        if not linked_account:
            raise GameAccountUnavailable()

        if not tournament.allow_free_users and user.subscription == SubscriptionType.FREE:
            raise FreeUserCannotJoinTournament()

        if tournament.minimum_profile_level and \
                tournament.minimum_profile_level > user.level and tournament.free_open_date > now:
            raise MinimumProfileLevelException()

        is_waiting_list = False
        if tournament.current_participants() >= tournament.max_participants:
            is_waiting_list = True
    
        try:
            participant = TournamentParticipant.objects.get_or_create(
                tournament=tournament,
                participant=user,
                defaults={
                    'is_waiting_list': is_waiting_list
                }
            )
        except IntegrityError:
            raise ParticipantExists()


        # if tournament.give_sticker:
        #     if user.stickers.all() :
        #         sticker = Sticker.objects.filter(
        #             ~Q(id__in=user.stickers.all())
        #         ).order_by('?').first()
        #         if sticker :
        #             user.stickers.add(sticker)
        #             user.save()

        if is_waiting_list:
            return Response(
                {"code": "waiting_list",
                 "message": "You have been added to the waiting list."},
                status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_200_OK)

    # TODO: must be fixed and updated on the frontend
    @action(detail=False, methods=['get'], permission_classes=(permissions.AllowAny,))
    def get_participants(self, request):
        slug = self.request.query_params.get('slug', None)

        if not slug:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            tournament = Tournament.objects.get(
                slug=slug,
                regions__in=[request.region]
            )

        except Tournament.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        participants = tournament.participants()


        page_number = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('size', 20)

        paginator = Paginator(participants, page_size)
        try:
            participants = paginator.page(int(page_number))
        except:
            participants = paginator.page(1)

        serializer = TournamentParticipantSerializer(participants, many=True)
        return Response({
            "data": serializer.data,
            "pagination": {
                "has_next": participants.has_next()
            }
        })

   
    @action(detail=False, methods=['get'], permission_classes=(permissions.AllowAny,))
    def get_tournaments(self, request):
        page_number = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('size', 6)
        state = self.request.query_params.get('state', TournamentState.UPCOMING)
        game = self.request.query_params.get('game', 0)
        user = self.request.user
        now = timezone.now()
        tournament_list =  Tournament.objects.select_related('game').prefetch_related(
                'tournamentparticipant_set',
                Prefetch(
                    'tournamentprize_set',
                    queryset=TournamentPrize.objects.order_by('position')
                )).filter(regions__in=[self.request.region])
        if game != '0' :
            tournament_list = tournament_list.filter(game__id=int(game))
        
        if not user.is_authenticated:
            tournament_list = tournament_list.filter(
                free_open_date__lte=now,
            ).annotate(live_null=Count('live_link'),started_null=Count('started_on')) 
        else :
            tournament_list = tournament_list.annotate(
                is_min_level=Case(
                    When(Q(minimum_profile_level__isnull=False) &
                         Q(minimum_profile_level__gt=user.level),
                         then=False),
                    default=True
                )
            ).filter(
                 Q(free_open_date__lte=now) |
                (Q(Q(minimum_profile_level__lte=user.level) | Q(minimum_profile_level__isnull=True)) & Q(free_open_date__gt=now))
            ).annotate(live_null=Count('live_link'),started_null=Count('started_on'))
        upcoming = tournament_list.filter(end_date__gte=now,started_on__isnull=True).order_by('start_date')
        ongoing = tournament_list.filter(end_date__gt=now,started_on__isnull=False).order_by('-live_null', 'start_date')
        previous = tournament_list.filter(end_date__lt=now)
        exceptprevioustournaments = list(ongoing) + list(upcoming)
        if state == TournamentState.UPCOMING:
            tournaments = upcoming
        elif state == TournamentState.PAST:
            tournaments =  previous
        elif state == TournamentState.ONGOING:
            tournaments = ongoing
        else:
            tournaments = list(exceptprevioustournaments) + list(previous) # tournament_list.all().order_by('id')  # added order to remove warning
        
        paginator = Paginator(tournaments, page_size)
        all_paginator = Paginator(exceptprevioustournaments, page_size)
        try:
            tournaments = paginator.page(int(page_number))
            exceptprevioustournaments = all_paginator.page(int(page_number))
        except:
            tournaments = paginator.page(1)
            exceptprevioustournaments = all_paginator.page(1)
            
        serializer = TournamentSerializer(paginator.page(int(page_number)), many=True, context={'requesto': request})
        upcomingserializer = TournamentSerializer(upcoming, many=True, context={'requesto': request})
        allserializer = TournamentSerializer(exceptprevioustournaments, many=True, context={'requesto': request})
        return  Response({
            "data": serializer.data,
            "tournaments": upcomingserializer.data,
            "all_serializer": allserializer.data,
            "pagination": {
                "pages":paginator.num_pages,
                "all_pages":all_paginator.num_pages
            },
            
        })  
        

class TournamentPrizeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TournamentPrize.objects.select_related(
        'tournament').exclude(image='')
    serializer_class = TournamentPrizeSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_fields = ('prize_type',)

    def get_queryset(self):
        now = timezone.now()
        return self.queryset.filter(
            tournament__regions__in=[self.request.region],
            tournament__end_date__gt=now
        ).exclude(image='')


class TournamentWinnerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TournamentPrize.objects.all()
    serializer_class = TournamentWinnerSerializer
    permission_classes = (permissions.AllowAny,)

    # def list(self, request, *args, **kwargs):
    #     try:
    #         game = request.query_params['game']
    #     except KeyError:
    #         raise ValidationError('Game parameter is missing')

    #     queryset = TournamentPrize.objects.filter(
    #         winner__isnull=False,
    #         tournament__game__slug__iexact=game,
    #         tournament__regions__in=[request.region]
    #     ).values('winner').annotate(
    #         winner_name=F('winner__nickname'),
    #         win_count=Count('winner')
    #     ).values('winner_name').order_by('-win_count').all()[:10]

    #     return Response(list(queryset), status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
       
        game = request.query_params['game']
        tournament = request.query_params['tournament']

        if game and game!= '':
            queryset = TournamentPrize.objects.filter(
                winner__isnull=False,
                tournament__id=tournament,
                tournament__game__slug__iexact=game,
                tournament__regions__in=[request.region]
            ).values('winner').annotate(
                winner_name=F('winner__nickname'),
                win_count=Count('winner')
            ).values('winner_name').order_by('-win_count').all()
        else :
            queryset = TournamentPrize.objects.filter(
                winner__isnull=False,
                tournament__id=tournament,
                tournament__regions__in=[request.region]
            ).values('winner').annotate(
                winner_name=F('winner__nickname'),
                win_count=Count('winner')
            ).values('winner_name').order_by('-win_count').all()
        return Response(list(queryset), status=status.HTTP_200_OK)