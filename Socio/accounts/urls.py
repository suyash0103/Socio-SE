from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('createFace/', views.createFace, name="createFace"),
    path('createFaceEncoding/', views.createFaceEncoding, name="createFaceEncoding"),
    path('face/', views.face, name="face"),
    path('loginFace/', views.loginFace, name="uploadFace"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('password-change/', views.PasswordChangeView.as_view(),name='password-change'),
]
