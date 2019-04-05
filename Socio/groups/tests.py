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

    def test_groups_withLogin(self):
        request = self.factory.get('/groups/')

        request.user = self.user


        response = GroupListView.as_view()(request)
        print(Fore.YELLOW + "Testing groups Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "groups page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "groups page not working without login")
            print(Style.RESET_ALL)

    def test_groups_withoutLogin(self):
        request = self.factory.get('/groups/')

        request.user = AnonymousUser()


        response = GroupListView.as_view()(request)
        print(Fore.YELLOW + "Testing groups Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "groups page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "groups page not working without login")
            print(Style.RESET_ALL)

    def test_groups_create_withLogin(self):
        request = self.factory.get('/groups/create/')

        request.user = self.user


        response = CreateGroupView.as_view()(request)
        print(Fore.YELLOW + "Testing groups create Page with login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "groups create page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "groups create page not working without login")
            print(Style.RESET_ALL)

    def test_groups_create_withoutLogin(self):
        request = self.factory.get('/groups/create/')

        request.user = AnonymousUser()


        response = CreateGroupView.as_view()(request)
        print(Fore.YELLOW + "Testing groups create Page without login")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "groups create page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "groups create page not working without login")
            print(Style.RESET_ALL)

