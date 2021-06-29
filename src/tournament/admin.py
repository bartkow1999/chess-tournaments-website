from django.contrib import admin
from src.tournament.models import Tournament, Entry, Ranking, Match

admin.site.register(Tournament)
admin.site.register(Entry)
admin.site.register(Ranking)
admin.site.register(Match)

