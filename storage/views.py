from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpRequest
from django.db.models import Count

from storage.models import Storage, Truck
from lib.filter_storages_params import GetParamsFilter


def index(request: HttpRequest):
    filter_service = GetParamsFilter(request.GET)
    if not filter_service.is_valid:
        return HttpResponse(content='invalid request params', status=422)

    storage_list = Storage.objects.annotate(trucks_count=Count('truck')).order_by(filter_service.sort_string)
    context = {
        'storage_list': storage_list,
        'change_to': filter_service.params['change_to'],
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
