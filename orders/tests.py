from django.test import TestCase, LiveServerTestCase
from perinone.testing import *


class OrdersTests(LiveServerTestCase):

    def test_stuff(self):
        with WebTester(self.live_server_url, "/orders/") as web:
            web.expect("Hello!")


