from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpRequest, JsonResponse

from storage.models import Storage, Truck

from lib.storages_services import GetStoragesService
from lib.clients.weather_client import WeatherApiClient
from lib.forms_factory import FormsFactory
from lib.notificators import FlashNotifier


def index(request: HttpRequest):
    storages_params = FormsFactory.produce('filter-storages', params=request.GET)
    storage_list = GetStoragesService(form=storages_params).list

    if request.GET.get('table_only'):
        return render(request, 'storage/storages_table.html', {'storage_list': storage_list})

    create_form = FormsFactory.restore_by_key(request.GET.get('storage_form_id'), 'storage')
    context = {
        'storage_list': storage_list,
        'form': create_form,
        'filter_form': storages_params
    }
    return render(request, 'storage/index.html', context)


def detail(request: HttpRequest, storage_id):
    truck_list = Truck.objects.filter(current_storage=storage_id)
    current_storage = get_object_or_404(Storage, id=storage_id)

    notifier = FlashNotifier(request)
    notifier.info(f'Welcome to page {request.get_full_path()}')
    notifier.error('It is error! god damn!')

    context = {
        'truck_list': truck_list,
        'current_storage': current_storage
    }
    return render(request, 'storage/detail.html', context)


def create_storage(request: HttpRequest):
    form = FormsFactory.produce('storage', params=request.POST)
    if form.is_valid():
        storage = Storage(
            location=form.cleaned_data.get("location"),
            name=form.cleaned_data.get("name"),
            capacity=form.cleaned_data.get("capacity")
        )
        storage.save()
        return redirect(reverse('all-storages'))
    else:
        uuid = FormsFactory.save_state(request.POST)
        return redirect(reverse('all-storages') + '?' + f"storage_form_id={uuid}")


def show_current_weather(request: HttpRequest):
    notifier = FlashNotifier(request)

    location = request.GET.get("location")
    if not location:
        notifier.error("no location provided")
        return redirect(reverse('all-storages'))

    current_weather = WeatherApiClient(location).current()
    if not current_weather['is_successful']:
        error = current_weather['response_body']['error']
        notifier.error(error.get('message', 'Something went wrong. Try later'))
        return redirect(reverse('all-storages'))

    data = current_weather['response_body']
    w = {
        'country': data['location']['country'],
        'city': data['location']['name'],
        'upd': data['current']['last_updated'],
        'cond': data['current']['condition']['icon'],
        'temp': data['current']['temp_c'],
        'wind': data['current']['wind_kph']
    }

    img = f'<img src="{w["cond"]}" width = "20" height = "20">'
    msg = f'Weather in {w["country"]} {w["city"]} at {w["upd"]}: {img} t: {w["temp"]} C°, w: {w["wind"]} km / h'

    notifier.info(msg, delay=10_000)
    return redirect(reverse('all-storages'))
