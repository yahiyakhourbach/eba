from rest_framework import serializers
from booking.models import Booking
from .models import Event

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model= Event
        fields = "__all__"

class regularEventSerializer(serializers.ModelSerializer):

    isBooking = serializers.SerializerMethodField()
    class Meta:
        model= Event
        fields = "__all__"
    
    def get_isBooking(self, obg):
        user = self.context["request"].user
        booking  = Booking.objects.filter(user=user,event=obg).exists()
        return booking