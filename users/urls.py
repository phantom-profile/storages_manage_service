from django.urls import path, include
from django.contrib.auth import views as auth_views

from users import views

# users/login/ [name='login']
# users/logout/ [name='logout']
# users/password_change/ [name='password_change']
# users/password_change/done/ [name='password_change_done']
# users/password_reset/ [name='password_reset']
# users/password_reset/done/ [name='password_reset_done']
# users/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# users/reset/done/ [name='password_reset_complete']

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('cards/', views.index, name='cards'),
    path('convert_currency/', views.convert_currencies, name='convertor'),
    path("", include("django.contrib.auth.urls"))
]
