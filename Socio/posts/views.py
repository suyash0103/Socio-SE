from django.views import generic
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json,mimetypes,os
from .models import *
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str

# Create your views here.

User= get_user_model()

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    model=Post
    fields = ['title','text','image','file']

    def dispatch(self, request, *args, **kwargs):
        sender = request.user
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.is_valid():
            form.save()
            if form.instance.file:
                post = Post.objects.get(file=form.instance.file)
                post.sha1 = post.getSha1()
                post.save()
            return redirect('home')

class EditPostView(LoginRequiredMixin,UpdateView):
    login_url = '/login'
    model=Post
    fields = ['title','text','image','file']

    def dispatch(self, request, *args, **kwargs):
        pk=kwargs['pk']
        if request.user != Post.objects.get(pk=pk).owner:
            return redirect('posts:allPosts')
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            post = Post.objects.get(file=form.instance.file)
            post.sha1 = post.getSha1()
            post.save()
            return redirect('home')



class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Post
    success_url = reverse_lazy('posts:allPosts')

    def dispatch(self, request, *args, **kwargs):
        pk=kwargs['pk']
        if request.user != Post.objects.get(pk=pk).owner:
            return redirect('posts:allPosts')
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


def downloadFile(request,file_name):
    file_path = 'posts/uploads/'+file_name
    data = open(file_path, 'rb')
    sha = sha1.sha1(data)
    post = Post.objects.get(file=file_path)
    context = {'file': file_name}
    if sha == post.sha1:
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


@login_required(login_url='/login')
def postsView(request):
    try:
        p=set(request.user.post_owner.all())
        data={}
        suggestions=[]
        for friend in request.user.profile.friends.all():
            p=p.union(set(friend.post_owner.all()))
            for f in friend.profile.friends.all():
                if f not in request.user.friends.all() and f not in suggestions and f != request.user:
                    suggestions.append(f)

        context={
            'all_posts':reversed(list(p)),
            'user':request.user,
            'friends':request.user.profile.friends.count(),
            'groups':request.user.group_member.all(),
            'suggestions': suggestions,
        }
    except:
        context = {
            'user': request.user,

        }
    data = {
        'context': context,
    }
    return render(request,'posts/posts.html',data)



class LikePostView(LoginRequiredMixin, APIView):
    login_url =  '/login'
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        post=Post.objects.get(pk=pk)
        likes = int(post.likes.count())

        if request.user in post.likes.all():
            likes = likes-1
            liked = False
            post.likes.remove(request.user)
        else:
            liked = True
            likes = likes + 1
            post.likes.add(request.user)

        data = {
            'liked': liked,
            'likes': likes
        }
        return Response(data)

@csrf_exempt
def likePost(request):
    if request.method == 'POST':
        like_obj = json.loads(request.body.decode('utf-8'))

        post = Post.objects.get(pk=like_obj['post_id'])
        user = User.objects.get(username=like_obj['user'])

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        return HttpResponse("success")

    else:
        return HttpResponseRedirect('/')

class CommentPostView(LoginRequiredMixin, APIView):
    login_url =  '/login'
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        post=Post.objects.get(pk=pk)
        comment = Comment()
        comment.post = post
        comment.owner = request.user
        comment.text = request.GET['text']

        comment.save()
        data={
            'text':comment.text,
        }

        return Response(data)

@csrf_exempt
def commentPost(request):
    if request.method == 'POST':
        comment_obj = json.loads(request.body.decode('utf-8'))

        post = Post.objects.get(pk=comment_obj['post_id'])
        user = User.objects.get(username=comment_obj['user'])

        comment = Comment()
        comment.post = post
        comment.owner = user
        comment.text = comment_obj['comment_text']

        comment.save()

        return HttpResponse("success")

    else:
        return HttpResponseRedirect('/')

class GetUserView(LoginRequiredMixin, APIView):
    login_url =  '/login'
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):

        user = User.objects.get(username=request.GET['user'])
        if user:
            data={
                'username':user.username,
                'picture':str(user.profile.picture),
                'firstName':user.profile.firstName,
                'lastName':user.profile.lastName,
            }
        else:
            data={}
        return Response(data)
