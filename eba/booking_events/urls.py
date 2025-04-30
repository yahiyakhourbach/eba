from django.urls import path
from .views import CreateEvenView,GetEvent,GetEvents,UpdateEvent
urlpatterns = [
    path("events/",CreateEvenView.as_view(),name="create-event"),
    path("events/<int:id>/",GetEvent.as_view(),name="get-event"), 
    path("events/all/",GetEvents.as_view(),name="get-all-events"),
    path("events/update/<int:id>/",UpdateEvent.as_view(),name="update-events"),


]
