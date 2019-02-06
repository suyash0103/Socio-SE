from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('all/profile',views.AllProfilesView.as_view(), name="allProfiles"),
    path('profile/friends', views.friendList, name="friendList"),
    path('profile/friends/<pk>', views.removeFriend, name="removeFriend"),
    path('profile', views.startView, name="startView"),
    path('profile/<username>', views.ProfileView.as_view(), name="profileView"),
    path('profile/edit/<pk>', views.UpdateProfileView.as_view(), name="editProfile"),
    path('profile/create/<pk>', views.CreateProfileView.as_view(), name="createProfile"),

]