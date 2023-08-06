from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpRequest

from storage.models import Storage, Truck

from lib.storages_services import GetStoragesService, GetWeatherService
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
    GetWeatherService(
        location=request.GET.get("location", ''),
        notifier=FlashNotifier(request)
    ).perform()

    return redirect(reverse('all-storages'))
