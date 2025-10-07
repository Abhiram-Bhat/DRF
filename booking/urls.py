from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, MovieListView, movie_shows, ShowBookView, CancelBookingView, MyBookingsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/shows/', movie_shows, name='movie_shows'),

    path('shows/<int:pk>/book/', ShowBookView.as_view(), name='show_book'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='booking_cancel'),
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
]
