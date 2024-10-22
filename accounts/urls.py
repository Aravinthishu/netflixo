from django.contrib import admin
from django.urls import path, include
from .views import *
from allauth.account import views as allauth_views

urlpatterns = [
    path('profile', profile_view, name="profile" ),
    
    path('password/reset/', allauth_views.password_reset, name="account_reset_password"),
    path('password/reset/done/', allauth_views.password_reset_done, name="account_reset_password_done"),
    path('password/reset/key/<uidb64>/<key>/', allauth_views.password_reset_from_key, name="account_reset_password_from_key"),
    path('password/reset/key/done/', allauth_views.password_reset_from_key_done, name="account_reset_password_from_key_done"),

]
