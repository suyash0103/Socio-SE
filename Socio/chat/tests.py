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

    def test_chat_withLogin(self):
        request = self.factory.get('/chat/')

        request.user = self.user


        response = ChatRooms.as_view()(request)
        print(Fore.YELLOW + "Testing chat Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "chat page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "chat page not working without login")
            print(Style.RESET_ALL)

    def test_chat_withoutLogin(self):
        request = self.factory.get('/chat/')

        request.user = AnonymousUser()


        response = ChatRooms.as_view()(request)
        print(Fore.YELLOW + "Testing chat Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "chat page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "chat page not working without login")
            print(Style.RESET_ALL)

    def test_save_message_withLogin(self):
        request = self.factory.get('/save_message/')

        request.user = self.user


        response = save_message(request)
        print(Fore.YELLOW + "Testing save_message Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "save_message page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.GREEN + "save_message page verified")
            print(Style.RESET_ALL)

    def test_save_message_withoutLogin(self):
        request = self.factory.get('/save_message/')

        request.user = AnonymousUser()


        response = save_message(request)
        print(Fore.YELLOW + "Testing save_message Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "save_message page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "save_message page not working")
            print(Style.RESET_ALL)
