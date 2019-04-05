from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('groups', views.GroupListView.as_view(), name="groupList"),
    path('groups/create', views.CreateGroupView.as_view(), name="createGroup"),
    path('groups/edit/<pk>', views.UpdateGroupView.as_view(), name="updateGroup"),
    path('groups/delete/<pk>', views.DeleteGroupView.as_view(), name="deleteGroup"),
    path('groups/leave/<pk>', views.leaveGroup, name="leaveGroup"),
    path('groups/members/<pk>', views.addMember, name="members"),
    path('groups/add-member/<pk>', views.AddMemberView.as_view(), name="addMember"),
    path('groups/add-admin/<pk>', views.AddAdminView.as_view(), name="addAdmin"),
    path('groups/<name>',views.GroupView.as_view(),name="groupDetail"),
    path('groups/createPost/<pk>',views.CreatePost.as_view(),name="createPost"),


]