from django.urls import path

from storage import views

urlpatterns = [
    path('index', views.index, name='all-storages'),
    path('<int:storage_id>/detail', views.detail, name='one-storage'),
]
