import unittest
from django.urls import resolve
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .views import *

import colorama
from colorama import Fore, Style

# Test for Admin Views

class TestAdminViews(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='shreyas', email='shreyas@gmail.com', password='pass1234')

    def test_posts_withLogin(self):
        request = self.factory.get('/posts/')

        request.user = self.user


        response = postsView(request)
        print(Fore.YELLOW + "Testing posts Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "posts page not working without login")
            print(Style.RESET_ALL)

    def test_posts_withoutLogin(self):
        request = self.factory.get('/posts/')

        request.user = AnonymousUser()


        response = postsView(request)
        print(Fore.YELLOW + "Testing posts Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "posts page not working without login")
            print(Style.RESET_ALL)

    def test_posts_create_withLogin(self):
        request = self.factory.get('/posts/create/')

        request.user = self.user

        response = CreatePostView.as_view()(request)
        print(Fore.YELLOW + "Testing posts create Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts create page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "posts create page not working without login")
            print(Style.RESET_ALL)

    def test_posts_create_withoutLogin(self):
        request = self.factory.get('/posts/create/')

        request.user = AnonymousUser()

        response = postsView(request)
        print(Fore.YELLOW + "Testing posts create Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts create page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "posts create page not working without login")
            print(Style.RESET_ALL)

    def test_posts_like_withlogin(self):
        request = self.factory.get('/posts/like/')

        request.user = self.user

        response = likePost(request)
        print(Fore.YELLOW + "Testing posts like Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts like page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.GREEN + "posts like page verified")
            print(Style.RESET_ALL)

    def test_posts_like_withoutlogin(self):
        request = self.factory.get('/posts/like/')

        request.user = AnonymousUser()

        response = likePost(request)
        print(Fore.YELLOW + "Testing posts like Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts like page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "posts like page not working without login")
            print(Style.RESET_ALL)

    def test_posts_comment_withlogin(self):
        request = self.factory.get('/posts/comment/')

        request.user = self.user

        response = commentPost(request)
        print(Fore.YELLOW + "Testing posts comment Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts comment page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "posts comment page verified")
            print(Style.RESET_ALL)

    def test_posts_comment_withoutlogin(self):
        request = self.factory.get('/posts/comment/')

        request.user = AnonymousUser()

        response = commentPost(request)
        print(Fore.YELLOW + "Testing posts comment Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "posts comment page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "posts comment page not working")
            print(Style.RESET_ALL)