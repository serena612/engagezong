# coding: utf-8
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import  timedelta
from .models import Tournament, TournamentPrize, TournamentParticipant


UserModel = get_user_model()


class ReadOnlyTournamentPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentPrize
        fields = '__all__'


class ReadOnlyTournamentSerializer(serializers.ModelSerializer):
    state = serializers.CharField(read_only=True)

    class Meta:
        model = Tournament
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    current_participants = serializers.IntegerField(read_only=True)
    is_sold_out = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    is_closed = serializers.SerializerMethodField()
    starts_in = serializers.CharField(source='starts_in_full')
    prizes = ReadOnlyTournamentPrizeSerializer(source='tournamentprize_set',
                                               many=True, read_only=True)
    is_participant = serializers.SerializerMethodField()
    game_name = serializers.SerializerMethodField()
    top_winners = serializers.SerializerMethodField()
    tournament_started = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = '__all__'
    
    def get_game_name(self,obj):
        return obj.game_name()
    
    def get_top_winners(self,obj):
        if obj.is_closed():
            return obj.get_top_winners()
        else :
            return None    
    
    
    def get_is_sold_out(self, obj):
        if not obj.max_participants:
            return False

        return obj.is_sold_out()

    def get_is_participant(self, obj):
        try:
            # print(self.context['request'])
            user = self.context['requesto'].user
            
            gaga = obj.tournamentparticipant_set.filter(
                    participant=user)
            # print(gaga)
            if user.is_authenticated and gaga.exists():
                return True
            return False
        except:
            #print("Exception!!")
            return False   

    def get_is_closed(self, obj):
        return obj.is_closed()

    def get_is_expired(self, obj):
        return obj.is_expired()
    
    def get_tournament_started(self,obj):
        tournament_started = obj.start_date
        if obj.time_compared_to_gmt and int(obj.time_compared_to_gmt)>=0 :  # '+' in 
            tournament_started = obj.start_date + timedelta(hours=int(obj.time_compared_to_gmt))
        if obj.time_compared_to_gmt and int(obj.time_compared_to_gmt)<0 :  # '-' in 
            tournament_started = obj.start_date - timedelta(hours=int(obj.time_compared_to_gmt))
        return tournament_started

class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='nickname')
    country = serializers.SerializerMethodField()
    flag = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('uid', 'username', 'country', 'flag', 'avatar', 'level',
                  'profile_image')

    def get_country(self, obj):
        return obj.country.name

    def get_flag(self, obj):
        return f'/static/flags/{obj.country.code}.png'

    def get_avatar(self, obj):
        return obj.avatar.image.url if obj.avatar else None


class TournamentParticipantSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)

    class Meta:
        model = TournamentParticipant
        fields = ('id', 'participant', 'status', 'rank', 'created')


class TournamentPrizeSerializer(serializers.ModelSerializer):
    tournament = ReadOnlyTournamentSerializer()
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = TournamentPrize
        fields = '__all__'

    def get_participants_count(self, obj):
        return obj.tournament.current_participants()


class TournamentWinnerSerializer(serializers.Serializer):
    pass
