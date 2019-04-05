from django.views import generic
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
import mimetypes,os
from .models import *
from .forms import FileForm
# Create your views here.

User= get_user_model()

class CreateMessageView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    model=Message
    fields = ['message']

    def dispatch(self, request, *args, **kwargs):
        sender = request.user
        receiver = User.objects.get(username=self.kwargs['username'])
        if not receiver in set(sender.profile.friends.all()):
            return redirect('home')
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)

    def form_valid(self, form):
        sender = self.request.user
        receiver = User.objects.get(username=self.kwargs['username'])
        form.instance.sender = sender
        form.instance.receiver = receiver
        if form.is_valid():
            form.save()
            return redirect('home')

@login_required(login_url = "/login")
def SOS(request):
    sos = SOSMessage()
    sos.sender = request.user
    sos.save()
    return redirect('home')

@login_required(login_url='/login')
def location(request,pk):
    member = User.objects.get(pk=pk)
    context = {}
    context['member'] = member
    return render(request,"message/location.html",context)


class FileUploadView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    model=File
    fields = ['title','file']

    def dispatch(self, request, *args, **kwargs):
        sender = request.user
        receiver = User.objects.get(username=self.kwargs['username'])
        if not receiver in set(sender.profile.friends.all()):
            return redirect('home')
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)

    def form_valid(self, form):
        sender = self.request.user
        receiver = User.objects.get(username=self.kwargs['username'])
        form.instance.sender = sender
        form.instance.receiver = receiver

        if form.is_valid():
            form.save()
            file=File.objects.get(file=form.instance.file)
            file.sha1 = file.getSha1()
            file.save()
            return redirect('home')


class MessagesView(LoginRequiredMixin, generic.ListView):
    template_name='message/messages.html'
    context_object_name = 'all_messages'


    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        return reversed(user.message_receiver.all())


class SOSView(LoginRequiredMixin, generic.ListView):
    template_name = 'message/sos.html'
    context_object_name = 'all_messages'

    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        sos=[]
        for friend in user.profile.friends.all():
            for m in friend.sos_sender.all():
                sos.append(m)
        return sos

class FilesView(LoginRequiredMixin, generic.ListView):
    template_name='message/files.html'
    context_object_name = 'all_files'

    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        return reversed(user.file_receiver.all())

def downloadFile(request,file_name):
    file_path = 'message/uploads/'+file_name
    data = open(file_path, 'rb')
    sha = sha1.sha1(data)
    file = File.objects.get(file=file_path)
    context = {'file': file_name}
    if sha == file.sha1:
        file_wrapper = FileWrapper(open(file_path,'rb'))
        file_mimetype = mimetypes.guess_type(file_path)
        response = HttpResponse(file_wrapper, content_type=file_mimetype )
        response['X-Sendfile'] = file_path
        response['Content-Length'] = os.stat(file_path).st_size
        response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str(file_name)
        return response
    else:
        context['msg'] = 'was Altered'

    return render(request, 'message/check.html', context)


def checkFile(request,file_name):
    file_path = 'message/uploads/'+file_name
    data = open(file_path,'rb')
    sha = sha1.sha1(data)
    file=File.objects.get(file=file_path)
    context = {
        'file' : file_name
    }
    if sha==file.sha1:
        context['msg'] = 'was Unaltered.'
    else:
        context['msg'] = 'was Altered'

    return render(request,'message/check.html',context)