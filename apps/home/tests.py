# -*- encoding: utf-8 -*-
import unittest

from django.test import TestCase
from django.test import Client
import django.utils
from django.test.client import RequestFactory

from apps.home.views import wendler_view


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')
        # Test my_view() as if it were deployed at /customer/details
        response = wendler_view(request)
        self.assertEqual(response.status_code, 200)

c = Client()
response = c.post("/login/", {"username": "john", "password": "smith"})
response.status_code


# Create your tests here.
