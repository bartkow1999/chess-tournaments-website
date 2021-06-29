from django.shortcuts import render

from src.tournament.views import get_tournament_queryset
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

TOURNAMENTS_PER_PAGE = 3


def home_screen_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    tournaments = sorted(get_tournament_queryset(query), key=attrgetter('date_updated'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    tournaments_paginator = Paginator(tournaments, TOURNAMENTS_PER_PAGE)

    try:
        tournaments = tournaments_paginator.page(page)
    except PageNotAnInteger:
        tournaments = tournaments_paginator.page(TOURNAMENTS_PER_PAGE)
    except EmptyPage:
        tournaments = tournaments_paginator.page(tournaments_paginator.num_pages)

    context['tournaments'] = tournaments
    return render(request, "personal/home.html", context)
