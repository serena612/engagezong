# coding: utf-8
from datetime import timedelta

from django.utils import timezone

from engage.account.models import UserActivity, User
from engage.core.constants import NotificationTemplate
from engage.operator.models import Region
from engage.services import _with, notify_when
from django.utils.translation import activate, get_language
from django.utils.deprecation import MiddlewareMixin
from engage.settings.base import LANGUAGE_CODE
from contextlib import suppress

from django.conf import settings
from engage.tournament.models import Tournament
from django.utils import translation
from .models import UserNotification

class LastSeenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    @staticmethod
    def check_dormant_diff(last_seen, days):
        return timezone.now() - last_seen >= timedelta(days=days)

    @staticmethod
    @_with(log=True, threading=True)
    def update_last_seen(user):
        # this user was active on this day
        UserActivity.objects.set_active_day(current_user=user)

        last_seen = user.last_seen
        # update user last seen
        user.last_seen = timezone.now()
        user.save()

        if not last_seen:
            pass
        elif LastSeenMiddleware.check_dormant_diff(last_seen, 5):
            @notify_when(events=[NotificationTemplate.DORMANT_5_DAYS],
                         is_route=False, is_one_time=False)
            def notify(user, user_notifications):
                """ extra logic if needed """
            notify(user=user)
        elif LastSeenMiddleware.check_dormant_diff(last_seen, 3):
            @notify_when(events=[NotificationTemplate.DORMANT_3_DAYS],
                         is_route=False, is_one_time=False)
            def notify(user, user_notifications):
                """ extra logic if needed """
            notify(user=user)

        if not last_seen and  not user.is_complete_profile:
            @notify_when(events=[NotificationTemplate.COMPLETE_PROFILE],
                         is_route=False, is_one_time=False)
            def notify(user, user_notifications):
                """ extra logic if needed """
            notify(user=user)

        elif last_seen and (timezone.now().date() - last_seen.date()).days > 0 and not user.is_complete_profile:
            @notify_when(events=[NotificationTemplate.COMPLETE_PROFILE],
                         is_route=False, is_one_time=False)
            def notify(user, user_notifications):
                """ extra logic if needed """
            notify(user=user)
    
        

    def __call__(self, request):
        # TODO: to be cached


        request.region = Region.objects.get(id=1)
        

        language = get_language()
        print("Language"+ language)

        if request.user.is_authenticated:
            coins_received = UserNotification.objects.filter(
                    user=request.user,
                    notification__template=NotificationTemplate.DAILY,
                    created = timezone.now().date()).first()
            if not coins_received:
                self.update_last_seen(request.user)
            
            

        return self.get_response(request)
