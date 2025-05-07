from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from rest_framework.views import APIView
from .serializers import EventSerializer,regularEventSerializer
from users.permissions import IsModerator
from .models import Event

# Create your views here.


class GetEvents(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        search = request.GET.get("search",'')
        print("search :",search)
        if search:
            event = Event.objects.filter(title__icontains=search)
            if event.exists():
                serializer = regularEventSerializer(event,context={'request':request},many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({"error":"event not found"},status= status.HTTP_404_NOT_FOUND)

        if id:
            try:
                event =  Event.objects.get(id=id)
            except Event.DoesNotExist:
                return Response({"error":"event not found"},status= status.HTTP_404_NOT_FOUND)
            serializer = regularEventSerializer(event,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            events = Event.objects.all();
            serializer = EventSerializer(events, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)

class ManageEvents(APIView):

    permission_classes = [IsAuthenticated,IsModerator]

    def get(self, request, id = None):

        if id:
            try:
                event = Event.objects.get(id = id,user=request.user.id)
            except Event.DoesNotExist:
                return Response({"error" :"event doesn't exist"},status=status.HTTP_404_NOT_FOUND)

            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            events = Event.objects.filter(user=request.user.id)
            serializer = EventSerializer(events,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request,id=None):

        if id is not None:
            return Response({"detail" : "POST request should not inlcude an ID"}, status=status.HTTP_400_BAD_REQUEST)

        lat = request.data["location"]['lat']
        lng = request.data["location"]['lng']
        point = Point(float(lng),float(lat))

        event_data ={
            "user":request.user.id,
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
            

    def patch(self,request,id=None):

        if id is None:
            return Response({"error" : "missing id"},status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id = id, user = request.user.id)
        except Event.DoesNotExist:
            return Response({"error":"event not found"},status=status.HTTP_404_NOT_FOUND)
        
        event_data = None
        if 'location' in request.data:
            lng = request.data['location']['lng']
            lat = request.data['location']['lng']
            point = Point(float(lng),float(lat))
            event_data = request.data.copy()
            event_data['location'] = point
        
        serializer = EventSerializer(event,data=event_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id=None):

        if id is None:
            return Response({"error" : "missing id"},status=status.HTTP_400_BAD_REQUEST)

        
        event = Event.objects.filter(id=id, user = request.user.id).first()
        if event is None:
            return Response({"error":"event doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)