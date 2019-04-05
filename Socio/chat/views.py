from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import threading


# Create your views here.

User = get_user_model()

class ChatRooms(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    template_name = 'chat/chat-rooms.html'
    context_object_name = 'all_chats'

    def get_queryset(self):
        user = self.request.user
        q = user.chatroom_set.all()
        return q

@login_required(login_url='/login')
def chats(request,pk):
    room = ChatRoom.objects.get(pk=pk)
    if  request.user not in room.members.all():
        return redirect('home')
    cmsgs = ChatMessage.objects.filter(room=room).order_by('-date')[:50]
    msgs = []
    for msg in reversed(cmsgs):
        msgs.append(msg)
    context = {}
    context['room'] = room
    context['messages'] = msgs
    context['user'] = request.user
    return render(request, 'chat/chat_index.html', context)


@login_required(login_url='/login')
def location(request,pk,id):
    room = ChatRoom.objects.get(pk=pk)
    member = User.objects.get(pk=id)
    if request.user not in room.members.all():
        return redirect('home')
    context = {}
    context['room'] = room
    context['member'] = member
    return render(request,"chat/location.html",context)


@csrf_exempt
def save_message(request):
    # if the request method is a POST request
    if request.method == 'POST':
        # content sent via XMLHttpRequests can be accessed in request.body
        # and it comes in a JSON string, that's why we use json library to
        # turn it into a normal dictionary again
        msg_obj = json.loads(request.body.decode('utf-8'))

        # tries to create the message and save it in the db
        msg = ChatMessage()
        msg.room = ChatRoom.objects.get(pk=msg_obj['room'])
        msg.user = User.objects.get(username=msg_obj['user'])
        msg.text = msg_obj['message']
        msg.save()

        return HttpResponse("success")

    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def share_location(request):
    # if the request method is a POST request
    if request.method == 'POST':
        # content sent via XMLHttpRequests can be accessed in request.body
        # and it comes in a JSON string, that's why we use json library to
        # turn it into a normal dictionary again
        return HttpResponse("success")

    else:
        return HttpResponseRedirect('/')

