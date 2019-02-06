from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('requests',views.FriendRequestView.as_view(), name="friendRequests"),
    path('request/<pk>',views.newFriendRequest, name="newFriendRequest"),
    path('request/accept/<pk>',views.acceptRequest, name="acceptRequest"),
    path('request/reject/<pk>',views.rejectRequest, name="rejectRequest"),

]
