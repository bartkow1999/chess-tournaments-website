from operator import attrgetter

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from src.tournament.models import Tournament, Entry, Ranking, Match
from src.tournament.forms import CreateTournamentForm, UpdateTournamentForm, UpdateMatch1Form, UpdateMatch2Form
from src.account.models import Account


def create_tournament_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateTournamentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=request.user.email).first()
        obj.author = author
        obj.save()
        form = CreateTournamentForm()

    context['form'] = form

    return render(request, 'tournament/create_tournament.html', context)


def detail_tournament_view(request, slug):
    context = {}

    tournament = get_object_or_404(Tournament, slug=slug)
    context['tournament'] = tournament

    # user = request.user
    # author = Account.objects.filter(email=user.email).first()
    # entries = Entry.objects.filter(email=author)
    # context['entries'] = entries

    return render(request, 'tournament/detail_tournament.html', context)


def edit_tournament_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    tournament = get_object_or_404(Tournament, slug=slug)

    if tournament.author != user:
        return HttpResponse("You are not the author of that tournament.")

    if request.POST:
        form = UpdateTournamentForm(request.POST or None, request.FILES or None, instance=tournament)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            tournament = obj

    form = UpdateTournamentForm(
        initial={
            'title': tournament.title,
            'member_limit': tournament.member_limit,
            'date_tournament': tournament.date_tournament,
            'time_tournament': tournament.time_tournament,
            'date_deadline': tournament.date_deadline,
            'time_deadline': tournament.time_deadline,
            'location': tournament.location,
            'body': tournament.body,
            'image': tournament.image,
        }
    )
    context['form'] = form

    return render(request, 'tournament/edit_tournament.html', context)


def ranking_tournament_view(request, slug):
    context = {}

    tournament = get_object_or_404(Tournament, slug=slug)
    context['tournament'] = tournament

    matches = Match.objects.filter(tournament=tournament)
    for match in matches:
        if match.result_p1 == 1 and match.result_p2 == 1: # participant1 won
            obj = Ranking.objects.filter(tournament=tournament).filter(participant=match.participant1).first()
            obj.wins += 1
            obj.points += 3
            obj.save()
            obj = Ranking.objects.filter(tournament=tournament).filter(participant=match.participant2).first()
            obj.loses += 1
            obj.points -= 2
            obj.save()
            match.delete()
        elif match.result_p1 == -1 and match.result_p2 == -1: # participant2 won
            obj = Ranking.objects.filter(tournament=tournament).filter(participant=match.participant2).first()
            obj.wins += 1
            obj.points += 3
            obj.save()
            obj = Ranking.objects.filter(tournament=tournament).filter(participant=match.participant1).first()
            obj.loses += 1
            obj.points -= 2
            obj.save()
            match.delete()

    ranking_list = Ranking.objects.filter(tournament=tournament)
    ranking_list = sorted(ranking_list, key=attrgetter('points'), reverse=True)

    context['ranking_list'] = ranking_list

    return render(request, 'tournament/ranking_tournament.html', context)


def draw_tournament_view(request, slug):
    context = {}

    tournament = get_object_or_404(Tournament, slug=slug)
    entries = Entry.objects.filter(tournament=tournament)

    user = request.user
    if tournament.author != user:
        return HttpResponse("You are not the author of that tournament.")

    for entry in entries:
        obj = Ranking(
            tournament=tournament,
            participant=entry.email,
            wins=0,
            loses=0,
            points=0,
        )
        obj.save()

    ranking_list = Ranking.objects.filter(tournament=tournament)
    context['ranking_list'] = ranking_list

    for i in range(1, len(entries)):
        for j in range(i+1, len(entries)+1):
            obj = Match(
                tournament=tournament,
                participant1=entries[i-1].email,
                participant2=entries[j-1].email,
                result_p1=None,
                result_p2=None,
            )
            obj.save()


    context['tournament'] = tournament

    return render(request, 'tournament/ranking_tournament.html', context)


def entry_tournament_view(request, slug):
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")


    tournament = get_object_or_404(Tournament, slug=slug)
    author = Account.objects.filter(email=user.email).first()

    user = request.user
    if tournament.author == user:
        return HttpResponse("You are the author of that tournament.")

    entry = Entry.objects.filter(email=author).filter(tournament=tournament).first()
    if not entry:
        if tournament.member_limit > tournament.entry_counter:
            obj = Entry(email=author, tournament=tournament)
            obj.save()

            tournament.entry_counter += 1
            tournament.save()

            return render(request, "tournament/register_entry_positive.html", {})
        else:
            return render(request, "tournament/register_entry_limit_exceeded.html", {})
    else:
        return render(request, "tournament/register_entry_exists.html", {})


def match1_tournament_view(request, id):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    match = get_object_or_404(Match, id=id)

    user = request.user
    if user != match.participant1:
        return HttpResponse("You are not the first participant of that tournament.")

    if request.POST:
        form = UpdateMatch1Form(request.POST or None, request.FILES or None, instance=match)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            match = obj

    form = UpdateMatch1Form(
        initial={
            'result_p1': match.result_p1,
        }
    )
    context['form'] = form

    return render(request, 'tournament/match1_fill.html', context)


def match2_tournament_view(request, id):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    match = get_object_or_404(Match, id=id)

    user = request.user
    if user != match.participant2:
        return HttpResponse("You are not the second participant of that tournament.")

    if request.POST:
        form = UpdateMatch2Form(request.POST or None, request.FILES or None, instance=match)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            match = obj

    form = UpdateMatch2Form(
        initial={
            'result_p2': match.result_p2,
        }
    )
    context['form'] = form

    return render(request, 'tournament/match2_fill.html', context)


def get_tournament_queryset(query=None):
    queryset = []
    queries = query.split(" ") # python install 2019 = [python, install, 2019]
    for q in queries:
        tournaments = Tournament.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for tournament in tournaments:
            queryset.append(tournament)

    return list(set(queryset))
