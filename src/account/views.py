from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text

from src.account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from src.account.models import Account
from src.tournament.models import Tournament, Entry, Match

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from src.account.tokens import account_activation_token
from django.core.mail import send_mail


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/email_form.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'bartkow1999@gmail.com', [to_email])
            return render(request, 'account/email_confirmation.html', {})
            # return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'account/email_confirmation_positive.html', {})
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return render(request, 'account/email_confirmation_negative.html', {})
        # return HttpResponse('Activation link is invalid!')


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "name": request.POST['name'],
                "surname": request.POST['surname'],
                "username": request.POST['username'],
                "email": request.POST['email'],
                "license_number": request.POST['license_number'],
                "ranking": request.POST['ranking'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(
            initial={
                "name": request.user.name,
                "surname": request.user.surname,
                "username": request.user.username,
                "email": request.user.email,
                "license_number": request.user.license_number,
                "ranking": request.user.ranking,
            }
        )
    context['account_form'] = form

    tournaments = Tournament.objects.filter(author=request.user)
    context['tournaments'] = tournaments

    entries = Entry.objects.filter(email=request.user)
    context['entries'] = entries

    matches_p1 = Match.objects.filter(participant1=request.user)
    matches_p2 = Match.objects.filter(participant2=request.user)
    matches = matches_p1 | matches_p2
    context['matches'] = matches

    return render(request, 'account/account.html', context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
