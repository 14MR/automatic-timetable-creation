from django.test import TestCase
from rooms.models import ItemType
# Create your tests here.
from django.test import TestCase


class Test1(T):
    """This module has unit tests specified in test cases for first delivery"""

    def setUp(self):
        pass

    def test(self):
        it = ItemType()
        it.name = "test"
        self.assertEquals(it.name, "test")
