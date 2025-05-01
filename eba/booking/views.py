from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from events.models import Event
# Create your views here.


class ManageBooking(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):

        if id is not None:
            return Response({"detail" : "POST request should not inlcude an ID"}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(user = request.user.id)
        serializer = BookingSerializer(bookings,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request,id = None):

        if id is not None:
            return Response({"detail" : "POST request should not inlcude an ID"},status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=request.data["event"])
        except Event.DoesNotExist:
            return Response({"error":"event doesn't exist"},status = status.HTTP_404_NOT_FOUND)

        booking_data = request.data.copy()
        booking_data["user"] = request.user.id
        serializer = BookingSerializer(data=booking_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        
        if id is None:
            return Response({"error":"message error"}, status = status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.filter(user=request.user.id, event=id).first()
        if booking is None:
            return Response({"error":"not found"},status = status.HTTP_404_NOT_FOUND)
        
        print(booking)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

