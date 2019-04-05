from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect,reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib import messages
from authtools import views as authviews
from braces import views as bracesviews
from django.conf import settings
from . import forms
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

User = get_user_model()

def face(request):
    return render(request, 'accounts/face_login.html')

@login_required(login_url='/login')
def createFace(request):
    return render(request, 'accounts/create_face.html')

@csrf_exempt
@login_required(login_url='/login')
def createFaceEncoding(request):
    if request.POST:
        # save it somewhere
        f = open('accounts/userimages/temp.jpg', 'wb')
        b = base64.decodestring(request.body[23:])
        f.write(b)
        f.close()
        f=Face()
        f.user= request.user
        picture = face_recognition.load_image_file("accounts/userimages/temp.jpg")
        face_encoding = face_recognition.face_encodings(picture)[0]
        f.face_encoding = base64.b64encode(face_encoding)
        f.save()

        # return the URL
        return HttpResponse(request.user.username)
    else:
        return HttpResponse('')


@csrf_exempt
def loginFace(request):
    if request.POST:
        # save it somewhere
        f = open('accounts/webcamimages/temp.jpg', 'wb')
        b = base64.decodestring(request.body[23:])
        f.write(b)
        f.close()
        unknown_picture = face_recognition.load_image_file("accounts/webcamimages/temp.jpg")
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
        users = User.objects.all()
        for u in users:
            try :
                results = face_recognition.compare_faces([u.face.get_face_encoding()], unknown_face_encoding)
                print(u,results)
                if results[0]:
                    auth.login(request, u)
                    return HttpResponse(u)
            except:
                pass

        # return the URL
        return HttpResponse("")
    else:
        return HttpResponse('no data')


class LoginView(bracesviews.AnonymousRequiredMixin, authviews.LoginView):
    template_name = "accounts/login.html"
    form_class = forms.LoginForm


    def form_valid(self, form):
        r = super(LoginView, self).form_valid(form)
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me is True:
            ONE_MONTH = 30*24*60*60
            expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
            self.request.session.set_expiry(expiry)

        return redirect('home')


class LogoutView(authviews.LogoutView):
    url = reverse_lazy('home')


class SignUpView(bracesviews.AnonymousRequiredMixin,
                 bracesviews.FormValidMessageMixin,
                 generic.CreateView):
    form_class = forms.SignupForm
    model = User
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')
    form_valid_message = "You're signed up!"

    def form_valid(self, form):
        r = super(SignUpView, self).form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        return r


class PasswordChangeView(authviews.PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         "Your password was changed, "
                         "hence you have been logged out. Please relogin")
        return super(PasswordChangeView, self).form_valid(form)
