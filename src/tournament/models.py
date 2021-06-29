from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver


def upload_location(instance, filename, **kwargs):
    file_path = 'tournament/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id),
        title=str(instance.title),
        filename=filename
    )
    return file_path


class Tournament(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    member_limit = models.IntegerField(null=False, blank=False, default=8)
    # date_deadline = models.DateTimeField(verbose_name="date deadline")
    # date_tournament = models.DateTimeField(verbose_name="date tournament")
    date_tournament = models.DateField(verbose_name="date tournament")
    time_tournament = models.TimeField(verbose_name="time tournament")
    date_deadline = models.DateField(verbose_name="date deadline")
    time_deadline = models.TimeField(verbose_name="time deadline")
    entry_counter = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default="Poznan")

    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title


class Entry(models.Model):
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return self.tournament.title


class Ranking(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="participant", on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return str(self.participant)# + ' w:' + str(self.wins) + ' l:' + str(self.loses) + ' p:' + str(self.points)


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="participant1", on_delete=models.CASCADE)
    participant2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="participant2", on_delete=models.CASCADE)
    result_p1 = models.IntegerField(default=None, null=True)
    result_p2 = models.IntegerField(default=None, null=True)

    def __str__(self):
        if self.result_p1 is not None and self.result_p2 is not None:
            if self.result_p1 == self.result_p2:
                if self.result_p1 + self.result_p2 == 2:
                    return self.tournament.title + ': ' + str(self.participant1) + ' won against ' + str(self.participant2)
                if self.result_p1 + self.result_p2 == -2:
                    return self.tournament.title + ': ' + str(self.participant2) + ' won against ' + str(self.participant1)
        return self.tournament.title + ': ' + str(self.participant1) + ' vs ' + str(self.participant2)


@receiver(post_delete, sender=Tournament)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_tournament_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + instance.title)


pre_save.connect(pre_save_tournament_receiver, sender=Tournament)
