from rest_framework import serializers
from booking.models import Booking
from .models import Event

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model= Event
        fields = "__all__"
    
    def to_representation(self,instance):

        data = super().to_representation(instance)
        if instance.location:
            data["location"] = {
                "lng": instance.location.x,
                "lat": instance.location.y
            }
        else:
            data["location"] = None
        return data

class regularEventSerializer(serializers.ModelSerializer):

    isBooking = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    class Meta:
        model= Event
        fields = "__all__"
    
    def get_isBooking(self, obg):
        user = self.context["request"].user
        booking  = Booking.objects.filter(user=user,event=obg).exists()
        return booking
    
    def get_location(self,obj):
        if obj.location:
            return {
                "lng": obj.location.x,
                "lat": obj.location.y
            }
        return None