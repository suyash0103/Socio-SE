from django.views import generic
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
from groups.models import *
from posts.models import *
# Create your views here.


User = get_user_model()

class ProfileView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login'
    template_name='profiles/profile_view.html'
    context_object_name = 'context'

    def get_object(self, queryset=Profile.objects):
        user=User.objects.get(username=self.kwargs['username'])
        valid=False
        friendship="no"
        if self.request.user == user:
            valid = True
        else:
            sent=self.request.user.request_sender.all()
            received=user.request_receiver.all()
            if bool(set(sent) & set(received)):
                friendship="requested"
            if user in set(self.request.user.profile.friends.all()):
                friendship="friends"
        try:
            profile=Profile.objects.get(user=user)
            friends = profile.friends.count()
        except:
            profile=None

        p = set(user.post_owner.all())
        p = reversed(list(p))



        groups = user.group_member.all()

        return {'profile' :profile,'user':user,'valid':valid,'friendship':friendship, 'all_posts': p, 'friends':friends, 'groups': groups}

class AllProfilesView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    template_name = 'profiles/allProfiles.html'
    context_object_name = 'all_profiles'

    def get_queryset(self):
        query=self.request.GET['q']
        firstname = Profile.objects.filter(firstName__contains=query)
        lastName = Profile.objects.filter(lastName__contains=query)
        groupName = Group.objects.filter(name__contains=query)
        q=list(firstname.union(lastName))
        q.extend(list(groupName))
        return q


class CreateProfileView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login'
    model=Profile
    fields=['firstName','lastName','bio','picture']

    def dispatch(self, request, *args, **kwargs):
        user=User.objects.get(pk=self.kwargs['pk'])
        if self.request.user != user:
            try:
                logout(request.user)
            except:
                return redirect('accounts:login')
            return redirect('home')
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)

    def form_valid(self, form):
        user=User.objects.get(pk=self.kwargs['pk'])
        form.instance.user=user
        if form.is_valid():
            form.save()
            return redirect('profiles:profileView',user)


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login'
    model=Profile
    fields=['firstName','lastName','bio','picture']

    def dispatch(self, request, *args, **kwargs):
        user=User.objects.get(pk=self.kwargs['pk'])
        if self.request.user != user:
            try:
                logout(request.user)
            except:
                return redirect('accounts:login')
            return redirect('home')
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)


    def form_valid(self, form):
        user=User.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            form.save()
            return redirect('profiles:profileView',user)



@login_required(login_url='/login')
def friendList(request):
    context={
        'all_friends':request.user.profile.friends.all()
    }

    return render(request,'profiles/friendList.html',context)




@login_required(login_url='/login')
def removeFriend(request,pk):
    friend=User.objects.get(pk=pk)
    if friend not in request.user.profile.friends.all():
        return redirect('home')
    for room in request.user.chatroom_set.all():
        if room.members.count() == 2:
            if (request.user in room.members.all()) and (friend in room.members.all()):
                room.delete()
    request.user.profile.friends.remove(friend)
    friend.profile.friends.remove(request.user)
    return redirect('profiles:friendList')