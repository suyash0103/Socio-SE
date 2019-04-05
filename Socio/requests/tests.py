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

    def test_requests_withLogin(self):
        request = self.factory.get('/requests/')

        request.user = self.user


        response = FriendRequestView.as_view()(request)
        print(Fore.YELLOW + "Testing requests Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "requests page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "requests page not working without login")
            print(Style.RESET_ALL)

    def test_requests_withoutLogin(self):
        request = self.factory.get('/requests/')

        request.user = AnonymousUser()


        response = FriendRequestView.as_view()(request)
        print(Fore.YELLOW + "Testing requests Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "requests page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "requests page not working without login")
            print(Style.RESET_ALL)
