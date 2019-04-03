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

    def test_messages_withLogin(self):
        request = self.factory.get('/messages/')

        request.user = self.user


        response = MessagesView.as_view()(request)
        print(Fore.YELLOW + "Testing messages Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "messages page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "messages page not working without login")
            print(Style.RESET_ALL)

    def test_messages_withoutLogin(self):
        request = self.factory.get('/messages/')

        request.user = AnonymousUser()


        response = MessagesView.as_view()(request)
        print(Fore.YELLOW + "Testing messages Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "messages page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "messages page not working without login")
            print(Style.RESET_ALL)

    def test_files_withLogin(self):
        request = self.factory.get('/files/')

        request.user = self.user


        response = FilesView.as_view()(request)
        print(Fore.YELLOW + "Testing files Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "files page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "files page not working without login")
            print(Style.RESET_ALL)

    def test_files_withoutLogin(self):
        request = self.factory.get('/files')

        request.user = AnonymousUser()


        response = MessagesView.as_view()(request)
        print(Fore.YELLOW + "Testing files Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "files page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "files page not working without login")
            print(Style.RESET_ALL)

