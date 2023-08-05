from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from uuid import uuid4

from lib.users_services import CurrencyConverter, ConvertorError
from lib.forms_factory import FormsFactory
from users.models import CreditCard
from lib.clients.payment_client import PayServiceClient


@login_required
def profile(request):
    return render(request, 'profile.html', {'convertor_form': FormsFactory.produce('convertor')})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('storage:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def get_convertor(request):
    form = FormsFactory.produce('convertor', request.GET)
    return render(request, 'convertor_modal.html', {'convertor_form': form})


def convert_currencies(request):
    form = FormsFactory.produce('convertor', request.GET)
    if not form.is_valid():
        return JsonResponse({"error": form.errors}, status=422)

    try:
        converter = CurrencyConverter(
            convert_from=form.cleaned_data['convert_from'],
            convert_to=form.cleaned_data['convert_to'],
            amount=form.cleaned_data['amount_from']
        )
        convertion_result = converter.convert()
    except ConvertorError as e:
        return JsonResponse({"error": str(e)}, status=422)

    return JsonResponse(convertion_result, status=200)


def index(request):
    all_cards = CreditCard.objects.all()
    form = FormsFactory.produce('credit-card')
    context = {
        'cards': all_cards,
        'form': form
    }
    return render(request, 'index.html', context)


def trust_card(request):
    form = FormsFactory.produce('credit-card', params=request.POST)
    if form.is_valid():
        response = PayServiceClient().trust_card(
            card_number=form.cleaned_data.get("card_number"),
            cvv=form.cleaned_data.get("cvv"),
            owner=form.cleaned_data.get("owner"),
            bank=form.cleaned_data.get("bank"),
            vendor=form.cleaned_data.get("vendor")
        )
        if response["is_successful"]:
            card = CreditCard(
                card_number=form.cleaned_data.get("card_number"),
                cvv=form.cleaned_data.get("cvv"),
                owner=form.cleaned_data.get("owner"),
                bank=form.cleaned_data.get("bank"),
                vendor=form.cleaned_data.get("vendor"),
                expires_at=form.cleaned_data.get("expires_at"),
                card_uuid=response['response_body']['card_uuid']
            )
            card.save()
            return redirect(reverse('cards'))
        return redirect(reverse('cards'))
    return redirect(reverse('cards'))

