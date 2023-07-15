from django.urls import path

from storage import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('<int:storage_id>/detail', views.detail, name='detail'),
    path('vote', views.vote, name='vote'),
    path('results', views.results, name='results')
]
