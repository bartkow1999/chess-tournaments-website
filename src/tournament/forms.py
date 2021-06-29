from django import forms
from src.tournament.models import Tournament, Entry, Match


class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['title', 'member_limit', 'date_tournament', 'time_tournament', 'date_deadline', 'time_deadline', 'location', 'body', 'image']


class UpdateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['title', 'member_limit', 'date_tournament', 'time_tournament', 'date_deadline', 'time_deadline', 'location', 'body', 'image']

    def save(self, commit=True):
        tournament = self.instance
        tournament.title = self.cleaned_data['title']
        tournament.member_limit = self.cleaned_data['member_limit']
        tournament.date_tournament = self.cleaned_data['date_tournament']
        tournament.time_tournament = self.cleaned_data['time_tournament']
        tournament.date_deadline = self.cleaned_data['date_deadline']
        tournament.time_deadline = self.cleaned_data['time_tournament']
        tournament.location = self.cleaned_data['location']
        tournament.body = self.cleaned_data['body']

        if self.cleaned_data['image']:
            tournament.image = self.cleaned_data['image']

        if commit:
            tournament.save()

        return tournament


class RegisterEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['email', 'tournament']


class UpdateMatch1Form(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['result_p1']

    def save(self, commit=True):
        match = self.instance
        match.result_p1 = self.cleaned_data['result_p1']

        if commit:
            match.save()

        return match


class UpdateMatch2Form(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['result_p2']

    def save(self, commit=True):
        match = self.instance
        match.result_p2 = self.cleaned_data['result_p2']

        if commit:
            match.save()

        return match



