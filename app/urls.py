from django.urls import path
from .views import LoginView, CloupeCreateView, CoupleMessageCreateAPIView, CoupleMessageDetailAPIView, CoupleSpecialDateCreateAPIView, CoupleSpecialDateDetailAPIView, CoupleWishListCreateAPIView, CoupleWishListDetailAPIView, CoupleImageCreateAPIView, CoupleImageDetailAPIView, CoupleMessageOfTheDayAPIView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('couple/', CloupeCreateView.as_view(), name='couple-creation'),
    path('couple-messages/', CoupleMessageCreateAPIView.as_view(), name='create_couple_message'),
    path('couple-messages/<int:pk>/', CoupleMessageDetailAPIView.as_view(), name='couple_message_detail'),
    path('couple-specialdates/', CoupleSpecialDateCreateAPIView.as_view(), name='create_couple_special_date'),
    path('couple-specialdates/<int:pk>/', CoupleSpecialDateDetailAPIView.as_view(), name='couple_special_date_detail'),
    path('couple-wishlist/', CoupleWishListCreateAPIView.as_view(), name='create_couple_wishlist_item'),
    path('couple-wishlist/<int:pk>/', CoupleWishListDetailAPIView.as_view(), name='couple_wishlist_item_detail'),
    path('couple-images/', CoupleImageCreateAPIView.as_view(), name='create_couple_image'),
    path('couple-images/<int:pk>/', CoupleImageDetailAPIView.as_view(), name='couple_image_detail'),
    path('message-of-the-day/', CoupleMessageOfTheDayAPIView.as_view(), name='message_of_the_day'),
]