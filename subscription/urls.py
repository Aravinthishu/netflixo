from django.urls import path
from .views import *

urlpatterns = [
    path('plans/', subscription_plans, name='subscription_plans'),
    path('subscribe/<str:duration>/', subscribe, name='subscribe'),
]
