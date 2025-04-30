from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from rest_framework.views import APIView
from .serializers import EventSerializer
from users.permissions import IsModerator
from .models import Event
# Create your views here.


class GetEvent(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request,id):

        try:
            event =  Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error":"event not found"},status= status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UpdateEvent(APIView):

    permission_classes = [IsAuthenticated,IsModerator]

    def patch(self,request,id):

        event_data = None
        if 'location' in request.data:
            lng = request.data['location']['lng']
            lat = request.data['location']['lng']
            point = Point(float(lng),float(lat))
            event_data = request.data.copy()
            event_data['location'] = point

        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error":"event not found"},status=status.HTTP_404_BAD_REQUEST)
        serializer = EventSerializer(event,data=event_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_OK)

class GetEvents(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request):
        events = Event.objects.all()
        serializer = EventSerializer(events,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateEvenView(APIView):

    permission_classes = [IsAuthenticated,IsModerator]

    def post(self, request):
        lat = request.data["location"]['lat']
        lng = request.data["location"]['lng']
        point = Point(float(lng),float(lat))

        event_data ={
            "title":request.data["title"],
            "description":request.data["description"],
            "capacity":request.data["capacity"],
            "date" : request.data["date"],
            "location":point
        }

        serializer = EventSerializer(data = event_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



