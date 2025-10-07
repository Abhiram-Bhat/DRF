from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Show, Booking
from django.utils import timezone

class BookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.movie = Movie.objects.create(title='Test', duration_minutes=120)
        self.show = Show.objects.create(movie=self.movie, screen_name='A', date_time=timezone.now(), total_seats=2)

    def test_booking_creation(self):
        b = Booking.objects.create(user=self.user, show=self.show, seat_number=1)
        self.assertEqual(Booking.objects.filter(show=self.show, status='booked').count(), 1)
