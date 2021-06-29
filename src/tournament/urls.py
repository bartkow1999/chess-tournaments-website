from django.urls import path

from src.tournament.views import (
    create_tournament_view,
    detail_tournament_view,
    edit_tournament_view,
    entry_tournament_view,
    ranking_tournament_view,
    draw_tournament_view,
    match1_tournament_view,
    match2_tournament_view,
)

app_name = 'tournament'

urlpatterns = [
    path('create/', create_tournament_view, name="create"),
    path('<slug>/', detail_tournament_view, name="detail"),
    path('<slug>/edit/', edit_tournament_view, name="edit"),
    path('<slug>/ranking/', ranking_tournament_view, name="ranking"),
    path('<slug>/draw/', draw_tournament_view, name="draw"),
    path('<slug>/entry/', entry_tournament_view, name="entry"),
    path('<id>/match1/', match1_tournament_view, name="match1"),
    path('<id>/match2/', match2_tournament_view, name="match2"),
]
