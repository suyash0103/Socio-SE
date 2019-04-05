from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('message/create/<username>',views.CreateMessageView.as_view(), name="createMessage"),
    path('message',views.MessagesView.as_view(), name="messages"),
    path('generateSOS',views.SOS, name="generateSOS"),
    path('SOS',views.SOSView.as_view(), name="SOS"),
    path('SOS/location/<pk>', views.location, name='location'),
    path('files', views.FilesView.as_view(), name="files"),
    path('file/<username>',views.FileUploadView.as_view(), name="uploadFile"),
    path('download/<file_name>', views.downloadFile, name="download"),
    path('check/<file_name>', views.checkFile, name="check"),
]
