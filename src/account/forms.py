from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from src.account.models import Account


class RegistrationForm(UserCreationForm):
    # name = forms.CharField(max_length=30)
    # surname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ('name', 'surname', 'username', 'license_number', 'ranking', 'email', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login')


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'surname', 'username', 'license_number', 'ranking', 'email')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % account.email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % account.username)

    def clean_license_number(self):
        if self.is_valid():
            license_number = self.cleaned_data['license_number']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(license_number=license_number)
            except Account.DoesNotExist:
                return license_number
            raise forms.ValidationError('License number "%s" is already in use.' % account.license_number)

    def clean_ranking(self):
        if self.is_valid():
            ranking = self.cleaned_data['ranking']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(ranking=ranking)
            except Account.DoesNotExist:
                return ranking
            raise forms.ValidationError('Ranking "%d" is already in use.' % account.ranking)
