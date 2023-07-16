from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpRequest
from django.db.models import Count

from storage.models import Storage, Truck
from storage.forms import StorageForm


def index(request: HttpRequest):
    form = StorageForm()
    storage_list = Storage.objects.order_by('name').annotate(trucks_count=Count('truck'))
    context = {
        'storage_list': storage_list,
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
    return HttpResponse()
