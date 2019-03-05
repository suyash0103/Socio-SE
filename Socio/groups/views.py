from django.views import generic
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import *
from profiles.models import *
from chat.models import *
from posts.models import *
# Create your views here.


User = get_user_model()

class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login'
    model = Group
    fields = ['name', 'info', 'picture']

    def form_valid(self, form):
        user=self.request.user
        if form.is_valid():
            form.save()
            form.instance.admin.add(user)
            form.instance.members.add(user)
            chat = ChatRoom()
            chat.eid = form.instance.name
            chat.group = form.instance
            chat.save()
            chat.members.add(user)

            return redirect('groups:groupDetail',form.instance.name)

class UpdateGroupView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login'
    model = Group
    fields = ['name', 'info', 'picture']

    def dispatch(self, request, *args, **kwargs):
        user=self.request.user
        group=Group.objects.get(pk=self.kwargs['pk'])
        if user not in group.admin.all():
            return redirect('home')
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)


    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect('groups:groupDetail',form.instance.name)



class GroupView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login'
    template_name='groups/group_view.html'
    context_object_name = 'context'

    def get_object(self, queryset=Profile.objects):
        group=Group.objects.get(name=self.kwargs['name'])
        member=False
        admin=False
        all_posts=group.post_set.all()
        if self.request.user in group.admin.all():
            admin = True
        if self.request.user in group.members.all():
            member = True
        members=group.members.count()
        return {'group': group,'admin': admin, 'member': member, 'all_posts': all_posts,'members':members }

@login_required(login_url='/login')
def addMember(request,pk):
    group = Group.objects.get(pk=pk)
    if request.user not in group.admin.all():
        return redirect('home')
    return render(request,'groups/members.html',{'group':group})

class AddMemberView(LoginRequiredMixin, APIView):
    login_url =  '/login'
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        group=Group.objects.get(pk=pk)
        friend=User.objects.get(username=request.GET['friend'])

        if friend in group.members.all():
            group.members.remove(friend)
            group.chatroom.members.remove(friend)
            group.admin.remove(friend)
            status='removed'
        else:
            group.members.add(friend)
            group.chatroom.members.add(friend)
            status='added'

        data = {
            'status':status
        }
        return Response(data)

class AddAdminView(LoginRequiredMixin, APIView):
    login_url =  '/login'
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        group=Group.objects.get(pk=pk)
        friend=User.objects.get(username=request.GET['friend'])

        if friend in group.admin.all():
            group.admin.remove(friend)
            status='removed'
        else:
            group.admin.add(friend)
            status='added'

        data = {
            'status':status
        }
        return Response(data)


class GroupListView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    template_name = 'groups/group_list.html'
    context_object_name = 'all_groups'


    def get_queryset(self):
        q = self.request.user.group_member.all()
        return q

class DeleteGroupView(LoginRequiredMixin,generic.DeleteView):
    login_url = '/login'
    model = Group
    success_url = reverse_lazy('groups:groupList')

    def delete(self, request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['pk'])
        if self.request.user not in group.admin.all():
            return redirect('home')

        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

@login_required(login_url='/login')
def leaveGroup(request,pk):
    group=Group.objects.get(pk=pk)
    if request.user not in group.members.all():
        return redirect('home')
    group.members.remove(request.user)
    group.chatroom.members.remove(request.user)
    if group.members.count() == 0:
        group.delete()
    elif request.user in group.admin.all():
        group.admin.remove(request.user)
        if group.admin.count() == 0:
            group.admin.add(group.members.all()[0])

    return redirect('home')

class CreatePost(LoginRequiredMixin,CreateView):
    login_url = '/login'
    model=Post
    fields = ['title','text','image','file']

    def dispatch(self, request, *args, **kwargs):
        if request.user not in Group.objects.get(pk=self.kwargs['pk']).members.all():
            return redirect('home')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.group = Group.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            form.save()
            return redirect('home')
