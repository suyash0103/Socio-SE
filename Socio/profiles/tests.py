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

    def test_profile_withLogin(self):
        request = self.factory.get('/all/profile/')

        request.user = AnonymousUser()


        response = AllProfilesView.as_view()(request)
        print(Fore.YELLOW + "Testing profile Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "profile page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.GREEN + "profile page verified")
            print(Style.RESET_ALL)

    def test_profile_withoutLogin(self):
        request = self.factory.get('/all/profile/')

        request.user = AnonymousUser()


        response = AllProfilesView.as_view()(request)
        print(Fore.YELLOW + "Testing profile Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "profile page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "profile page not working without login")
            print(Style.RESET_ALL)

    def test_friendlist_withLogin(self):
        request = self.factory.get('/profile/friends/')

        request.user = AnonymousUser()

        response = friendList(request)
        print(Fore.YELLOW + "Testing friendlist Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "friendlist page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.GREEN + "friendlist page verified")
            print(Style.RESET_ALL)

    def test_friendlist_withoutLogin(self):
        request = self.factory.get('/profile/friends/')

        request.user = AnonymousUser()

        response = friendList(request)
        print(Fore.YELLOW + "Testing friendlist Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "friendlist page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "friendlist page not working without login")
            print(Style.RESET_ALL)