from django.shortcuts import render, HttpResponse
from django.http import HttpRequest


def index(request: HttpRequest):
    if request.GET.get('error'):
        return HttpResponse(content='You triggered error. Why??', status=400)

    return HttpResponse(content='Hello, it is root page', status=200)
