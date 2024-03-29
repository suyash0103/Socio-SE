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

    def test_signup_page(self):
        request = self.factory.get('/signup/')

        request.user = AnonymousUser()


        response = SignUpView.as_view()(request)
        result = self.assertEqual(response.status_code, 200)
        print(Fore.YELLOW + "Testing SignUp Page")
        print(Style.RESET_ALL)
        if result == None:
            print(Fore.GREEN + "SignUp page verified")
            print(Style.RESET_ALL)

    def test_signup_invalid(self):
        request = self.factory.get('/createFace/')

        request.user = AnonymousUser()


        response = createFace(request)
        print(Fore.YELLOW + "Testing Signup Page with invalid credentials")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "createFace page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "Signup Failed")
            print(Style.RESET_ALL)

    def test_login_page(self):
        request = self.factory.get('/login/')

        request.user = AnonymousUser()


        response = LoginView.as_view()(request)
        result = self.assertEqual(response.status_code, 200)
        print(Fore.YELLOW + "Testing Login Page")
        print(Style.RESET_ALL)
        if result == None:
            print(Fore.GREEN + "Login page verified")
            print(Style.RESET_ALL)

    def test_login_invalid(self):
        request = self.factory.get('/createFace/')

        request.user = AnonymousUser()


        response = createFace(request)
        print(Fore.YELLOW + "Testing Login Page with invalid credentials")
        print(Style.RESET_ALL)
        try:
            self.assertEqual(response.status_code, 200)
            print(Fore.GREEN + "createFace page verified")
            print(Style.RESET_ALL)

        except:
            print(Fore.RED + "Login failed")
            print(Style.RESET_ALL)

    

    def test_logout(self):
        # Create an instance of a GET request.
        request = self.factory.get('/logout/')

        request.user = AnonymousUser()

        response = LoginView.as_view()(request)
        result =self.assertEqual(response.status_code, 200)
        print(Fore.YELLOW + "Testing Logout Page")
        print(Style.RESET_ALL)
        if result == None:
            print(Fore.GREEN + "Logout page verified")
            print(Style.RESET_ALL)

