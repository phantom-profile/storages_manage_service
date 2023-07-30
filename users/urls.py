from django.urls import path
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('cards/', views.index, name='cards')
]
