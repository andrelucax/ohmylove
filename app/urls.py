from django.urls import path
from .views import LoginView, CloupeCreateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('couple/', CloupeCreateView.as_view(), name='couple-creation'),
]