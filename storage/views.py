from django.shortcuts import render, HttpResponse
from django.http import HttpRequest

from storage.models import Storage


def index(request: HttpRequest):
    storage_list = Storage.objects.order_by('name')
    context = {
        'storage_list': storage_list
    }
    return render(request, 'storage/index.html', context)


def detail(request: HttpRequest, storage_id):
    return HttpResponse("You're looking at storage %s." % storage_id)


def results(request: HttpRequest, storage_id):
    response = "You're looking at the results of storage %s."
    return HttpResponse(response % storage_id)


def vote(request: HttpRequest, storage_id):
    return HttpResponse("You're voting on storage %s." % storage_id)

