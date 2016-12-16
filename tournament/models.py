from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from picklefield.fields import PickledObjectField
from django.db.models.signals import m2m_changed, post_save
from django.core.exceptions import ValidationError


STATUS_CHOICES = (
    ('NS', 'Not started'),
    ('S', 'Started'),
    ('E', 'Ended'),
)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    photo = models.ImageField(null=True, blank=True)
    rank = models.PositiveSmallIntegerField(editable=False, default=30)

    def __str__(self):
        return '{f_n} {l_n}'.format(f_n=self.first_name, l_n=self.last_name)

    class Meta:
        pass


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NS')
    players = models.ManyToManyField(Player)

    def __str__(self):
        return self.name

    class Meta:
        pass


class Team(models.Model):
    name = models.CharField(max_length=150)
    goals = models.PositiveSmallIntegerField(default=0)
    misses = models.PositiveSmallIntegerField(default=0)
    tournament = models.ForeignKey(Tournament)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return self.name

    class Meta:
        pass


class Stage(models.Model):
    MODE_CHOICES = (
        ('REG', 'Regular'),
        ('PO', 'Playoff'),
    )
    mode = models.CharField(max_length=3, choices=MODE_CHOICES, default='REG')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return '{tour_name}: stage {st_id}({st_mode})'.format(
            tour_name=self.tournament.name,
            st_id=self.id,
            st_mode=self.mode,
        )


class Round(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, default='')

    def __str__(self):
        return '{tour_name}: stage {st_id}({st_mode}) | round {round_id}'.format(
            tour_name=self.tournament.name,
            st_id=self.stage.id,
            st_mode=self.stage.mode,
            round_id=self.id)

    class Meta:
        pass


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    score = PickledObjectField()

    def __str__(self):
        return '{tour_name}: round {round_id} | match {match_id}'.format(
            tour_name=self.round.tournament.name,
            round_id=self.round.id,
            match_id=self.id)

    class Meta:
        verbose_name_plural = 'matches'


def new_player(sender, instance, created, **kwargs):
    if created:
        player = Player.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
        )
        player.save()

post_save.connect(new_player, sender=User)


def teams_changed(sender, **kwargs):
    if kwargs['instance'].teams.count() > 2:
        raise ValidationError("You can't assign more than two teams")

m2m_changed.connect(teams_changed, sender=Match.teams.through)