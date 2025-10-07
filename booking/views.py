from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Movie, Show, Booking
from .serializers import SignupSerializer, MovieSerializer, ShowSerializer, BookingSerializer
from rest_framework.views import APIView

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.AllowAny,)

@api_view(['GET'])
def movie_shows(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    shows = movie.shows.all()
    serializer = ShowSerializer(shows, many=True)
    return Response(serializer.data)

class ShowBookView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        seat_number = request.data.get('seat_number')
        if seat_number is None:
            return Response({'detail':'seat_number required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            seat_number = int(seat_number)
        except:
            return Response({'detail':'seat_number must be integer'}, status=status.HTTP_400_BAD_REQUEST)

        if seat_number < 1 or seat_number > show.total_seats:
            return Response({'detail':'seat_number out of range'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                booked_count = Booking.objects.filter(show=show, status='booked').count()
                if booked_count >= show.total_seats:
                    return Response({'detail':'Show is fully booked'}, status=status.HTTP_400_BAD_REQUEST)

                booking = Booking.objects.create(user=request.user, show=show, seat_number=seat_number)
        except IntegrityError:
            return Response({'detail':'Seat already booked'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CancelBookingView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        if booking.user != request.user:
            return Response({'detail':'Cannot cancel others booking'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status == 'cancelled':
            return Response({'detail':'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({'detail':'Cancelled'}, status=status.HTTP_200_OK)

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
