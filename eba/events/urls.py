from django.urls import path
from .views import GetEvents,ManageEvents
urlpatterns = [

    # for moderators to manage thier events operations
    path("events/manage/", ManageEvents.as_view(), name="manage-events"),
    path("events/manage/<int:id>/", ManageEvents.as_view(), name="manage-events"),

    # for reguler users only to see available events
    path("events/",GetEvents.as_view(),name="get-events"),
    path("events/<int:id>/", GetEvents.as_view(), name="get-event")
]
