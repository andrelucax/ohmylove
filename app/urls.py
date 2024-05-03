from django.urls import path
from .views import LoginView, CloupeCreateView, CoupleMessageCreateAPIView, CoupleMessageDetailAPIView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('couple/', CloupeCreateView.as_view(), name='couple-creation'),
    path('couple-messages/', CoupleMessageCreateAPIView.as_view(), name='create_couple_message'),
    path('couple-messages/<int:pk>/', CoupleMessageDetailAPIView.as_view(), name='couple_message_detail'),
]