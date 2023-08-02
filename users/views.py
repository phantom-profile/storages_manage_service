from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from lib.users_services import CurrencyConverter, ConvertorError
from lib.forms_factory import FormsFactory
from users.models import CreditCard


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
    context = {
        'cards': all_cards
    }
    return render(request, 'index.html', context)
