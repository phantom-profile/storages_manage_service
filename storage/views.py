from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpRequest

from storage.models import Storage, Truck


def index(request: HttpRequest):
    storage_list = Storage.objects.order_by('name').prefetch_related('truck_set')
    context = {
        'storage_list': storage_list
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


def results(request: HttpRequest, storage_id):
    response = "You're looking at the results of storage %s."
    return HttpResponse(response % storage_id)


def vote(request: HttpRequest, storage_id):
    return HttpResponse("You're voting on storage %s." % storage_id)

