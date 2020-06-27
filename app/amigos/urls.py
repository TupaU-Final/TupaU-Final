from django.urls import path
from .views import *

app_name = "friends"

urlpatterns = [
    path('buscar_amigos', FindFriendsListView.as_view(), name="buscar"),
    path('send-request/<slug:username>', send_request, name="send-request"),
    path('accept-request/<slug:friend>', accept_request, name="accept-request"),
    path('rejected-request/<slug:friend>', rejected_request, name="rejected-request"),
]
