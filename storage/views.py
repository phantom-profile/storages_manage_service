from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from django.http import HttpRequest
from django.db.models import Count

from storage.models import Storage, Truck

from lib.filter_storages_params import GetParamsFilter
from lib.forms_factory import FormsFactory


def index(request: HttpRequest):
    form = FormsFactory.restore_by_key(request.GET.get('storage_form_id'), 'storage')
    filter_service = GetParamsFilter(request.GET)
    if not filter_service.is_valid:
        return HttpResponse(content='invalid request params', status=422)

    storage_list = Storage.objects.annotate(trucks_count=Count('truck')).order_by(filter_service.sort_string)
    context = {
        'storage_list': storage_list,
        'change_to': filter_service.params['change_to'],
        'form': form
    }
    return render(request, 'storage/index.html', context)


def detail(request: HttpRequest, storage_id):
    truck_list = Truck.objects.filter(current_storage=storage_id)
    current_storage = get_object_or_404(Storage, id=storage_id)
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
