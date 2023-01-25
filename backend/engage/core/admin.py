from django.contrib import admin
from django.db.models import Q
from engage.account.models import User
from jet.admin import CompactInline
from solo.admin import SingletonModelAdmin
from datetime import date, datetime
from engage.services import Notifications as NotificationsService
from . import models
from .constants import NotificationTemplate
from engage.services import notify_when, FCM

from parler.admin import TranslatableAdmin


class AvatarInline(admin.TabularInline):
    model = models.Avatar
    min_num = 0


@admin.register(models.Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    inlines = [AvatarInline]


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created')
    exclude = ('slug',)


@admin.register(models.Trophy)
class TrophyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')


@admin.register(models.Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')


@admin.register(models.HTML5Game)
class HTML5GameAdmin(admin.ModelAdmin):
    list_display = ('game', 'full_game_type', 'created', 'modified')
    exclude = ('slug',)

    def full_game_type(self, obj):
        return obj.get_game_type_display()
    full_game_type.vebose_name = 'Game Type'


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type',  'created', 'modified')


@admin.register(models.Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'action', 'free_user_points', 'paid1_user_points',
                    'paid2_user_points', 'created', 'modified')
    exclude = ('is_active',)


class BattlePassLevelAdmin(CompactInline):
    model = models.BattlePassLevel
    min_num = 1


@admin.register(models.BattlePass)
class BattlePassAdmin(admin.ModelAdmin):
    list_display = ('name', 'starts_at', 'ends_at', 'max_level', 'is_active',
                    'created', 'modified')
    inlines = [BattlePassLevelAdmin]


@admin.register(models.Notifications)
class NotificationAdmin(TranslatableAdmin): # admin.ModelAdmin
    list_display = ('template', 'action', 'title', 'is_active', 'created', 'modified')
    list_filter = ('is_active',)
    exclude = ('is_claimed', 'is_gift')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(~Q(template=NotificationTemplate.INSTANT))

    def save_model(self, request, obj, form, change):
        is_active = request.POST.get('is_active', 'off')
        template = request.POST.get('template', 'text')
        package = request.POST.get('package')
        super().save_model(request, obj, form, change)
        # if is_active == "on" and template == NotificationTemplate.INSTANT.value:
            # NotificationsService.bulk(obj)
            
            

    class Media:
        js = ('admin/notification/base.js',)


@admin.register(models.FeaturedGame)
class FeaturedGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
