from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpRequest
from django.db.models import Count

from storage.models import Storage, Truck


def index(request: HttpRequest):
    params = filter_params(request.GET)
    if not params:
        return HttpResponse(content='invalid request params', status=422)

    order_string = f"{params['order']}{params['sort']}"
    storage_list = Storage.objects.annotate(trucks_count=Count('truck')).order_by(order_string)
    context = {
        'storage_list': storage_list,
        'change_to': params['change_to'],
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


def filter_params(params: dict) -> dict:
    sort = params.get('sort', 'name')
    order = params.get('order', 'desc')
    if order not in ('asc', 'desc') or sort not in ('name', 'location', 'id', 'trucks_count'):
        return {}
    if order == 'desc':
        order = '-'
        change_to = 'asc'
    else:
        order = ''
        change_to = 'desc'
    return {'order': order, 'change_to': change_to, 'sort': sort}
