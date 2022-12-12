# coding: utf-8

from datetime import date, datetime
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from engage.core.models import Notifications
from engage.services import Notifications as NotificationsService
from engage.core.constants import WinAction, NotificationTemplate
from engage.core.models import BattlePassMission, Sticker
from engage.services import notify_when, FCM
from .constants import FriendStatus, CoinTransaction, Transaction, SubscriptionPlan
from .models import (
    User,
    Profile,
    UserNotification,
    FriendList,
    UserGamePlayed,
    UserBattlePassMission,
    SendCoinsHistory,
    UserFavoriteFriend, UserTransactionHistory
)



@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if not created:
        return

    Profile.objects.create(user=instance)
    instance.nickname = f'player{instance.id}'
    instance.save()


# listen for notifications
@receiver(post_save, sender=UserNotification)
def new_user_notification(sender, instance, created, **kwargs):
    if created:
        if not instance.is_sent:
            instance.is_sent = True
            instance.save()

            # send single fcm notification
            FCM.single(
                user=instance.user,
                title=instance.title,
                message=instance.text,
                data={
                    'action': instance.action,
                    'url': instance.url,
                    'template': instance.template
                },
                type=instance.type
            )

# listen for notifications
@receiver(m2m_changed, sender=Notifications.package.through)
def new_user_notification_package(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    package_ids = kwargs.pop('pk_set', None)
    package_list=[]
    now = datetime.now()
 
    for i in package_ids :
        if i == 1 :
            package_list.append(SubscriptionPlan.FREE)
        elif i == 2 :
            package_list.append(SubscriptionPlan.PAID1)  
        elif i == 3 :
            package_list.append(SubscriptionPlan.PAID2)       
    if instance.is_active  and instance.template == NotificationTemplate.INSTANT.value:
        users = User.objects.filter(subscription__in=package_list)
        NotificationsService.newbulk(instance,users)


@receiver(post_save, sender=FriendList)
def user_friend_add(sender, instance: FriendList, created, **kwargs):
    if created:
        # notify the user whom receive the friend request
        @notify_when(
            events=[NotificationTemplate.FRIEND_REQUEST],
            is_route=False,
            is_one_time=True,
            extra={
                "nickname": instance.user.nickname or instance.user.username,
                "friend": instance.friend.nickname or instance.friend.username
            }
        )
        def notify(user, user_notifications):
            # update user notification >> set friend uid
            for notification in user_notifications:
                notification.friend_uid = instance.user.uid
                notification.save()

        notify(instance.friend)
    else:
        # friend added successfully
        if instance.status == FriendStatus.ACCEPTED:
            # notify the user whom send the friend request
            @notify_when(
                events=[NotificationTemplate.FRIEND_ADDED],
                is_route=False,
                is_one_time=False,
                extra={
                    "nickname": instance.user.nickname or instance.user.username,
                    "friend": instance.friend.nickname or instance.friend.username
                }
            )
            def notify(user, user_notifications):
                """ extra logic if needed """

            notify(instance.user)


@receiver(post_delete, sender=FriendList)
def user_friend_remove(sender, instance, *args, **kwargs):
    UserFavoriteFriend.objects.filter(
        (Q(user=instance.user) & Q(friend=instance.friend)) |
        (Q(user=instance.friend) & Q(friend=instance.user))
    ).delete()


@receiver(post_save, sender=UserGamePlayed)
def user_game_played(sender, instance, created, **kwargs):
    now = datetime.now(tz=timezone.utc)

    # user battle pass >>  WinAction (play_game)
    try:
        today_battlepass = BattlePassMission.objects.select_related(
            'mission'
        ).get(
            date__year=now.year,
            date__month=now.month,
            date__day=now.day,
            mission__action__in=[WinAction.PLAY_GAME, WinAction.PLAY_2_GAMES]
        )
    except (BattlePassMission.DoesNotExist,
            BattlePassMission.MultipleObjectsReturned):
        return

    if today_battlepass.mission.action == WinAction.PLAY_GAME:
        obj, created = UserBattlePassMission.objects.select_related(
            'user',
            'bp_mission',
            'bp_mission__mission'
        ).get_or_create(
            bp_mission=today_battlepass,
            user=instance.user,
            is_completed=True
        )

        if created:
            @notify_when(
                events=[NotificationTemplate.MISSION_COMPLETED],
                is_route=False,
                is_one_time=False,
                extra={
                    "nickname": instance.user.nickname,
                }
            )
            def notify(user, user_notifications):
                """ extra logic if needed """

            notify(instance.user)
    else:
        obj, created = UserBattlePassMission.objects.select_related(
            'user',
            'bp_mission',
            'bp_mission__mission'
        ).get_or_create(
            bp_mission=today_battlepass,
            user=instance.user,
            defaults={'count': 1}
        )

        if not created and obj.count == 1:
            obj.count += 1
            obj.is_completed = True
            obj.save()

            @notify_when(
                events=[NotificationTemplate.MISSION_COMPLETED],
                is_route=False,
                is_one_time=False,
                extra={
                    "nickname": instance.user.nickname,
                }
            )
            def notify(user, user_notifications):
                """ extra logic if needed """

            notify(instance.user)




@receiver(post_save, sender=SendCoinsHistory)
@transaction.atomic()
def user_send_coins(sender, instance, created, **kwargs):
    if not created:
        return

    UserTransactionHistory.objects.create(
        user=instance.user,
        amount=-instance.amount,
        action=CoinTransaction.SEND,
        info = Transaction.SEND
    )

    UserTransactionHistory.objects.create(
        user=instance.receiver,
        amount=instance.amount,
        action=CoinTransaction.RECEIVE,
        info = Transaction.RECEIVE
    )
   
    @notify_when(
        events=[NotificationTemplate.SEND_COINS],
        is_route=False,
        is_one_time=False,
        extra={
            "nickname": instance.user.nickname,
            "amount": instance.amount
        }
    )
    def notify(user, user_notifications):
        """ extra logic if needed """

    notify(instance.receiver)
    instance.user.seen_coins = True
    instance.user.old_coins = instance.user.coins 
    instance.user.save()
    instance.receiver.seen_coins = False
    instance.receiver.save()
