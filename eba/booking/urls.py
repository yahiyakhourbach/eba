from django.urls import path
from .views import ManageBooking

urlpatterns = [
    path("bookings/", ManageBooking.as_view(),name="manage-bookings"),
    path("bookings/<int:id>/", ManageBooking.as_view(),name="manage-bookings")
]
