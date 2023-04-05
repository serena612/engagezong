from django.db import models
from django.db.models import Case, Value, When
from django.utils import timezone
from parler.managers import TranslatableQuerySet


class TournamentQuerySet(models.QuerySet): #models.QuerySet
    def past(self):
        now = timezone.now()
        return self.filter(
            end_date__lte=now
        )
    

    def ongoing(self):
        now = timezone.now()
        return self.filter(
            end_date__gte=now
        )

    def upcoming(self):
        now = timezone.now()
        return self.filter(
            start_date__gt=now,
        )

    def joined(self, user):
        return self.filter(
            tournamentparticipant__participant=user
        )

    def is_participant(self, user):
        return self.annotate(
            is_participant=Case(
                When(tournamentparticipant__participant=user, then=Value(True)),
                default=Value(False)
            )
        )
    
class TournamentTranslatableQuerySet(TranslatableQuerySet): #models.QuerySet
    def past(self):
        now = timezone.now()
        return self.filter(
            end_date__lte=now
        )
    

    def ongoing(self):
        now = timezone.now()
        return self.filter(
            end_date__gte=now
        )

    def upcoming(self):
        now = timezone.now()
        return self.filter(
            start_date__gt=now,
        )

    def joined(self, user):
        return self.filter(
            tournamentparticipant__participant=user
        )

    def is_participant(self, user):
        return self.annotate(
            is_participant=Case(
                When(tournamentparticipant__participant=user, then=Value(True)),
                default=Value(False)
            )
        )

class TournamentManager(models.Manager):
    def get_queryset(self):
        return TournamentQuerySet(self.model, using=self._db)
