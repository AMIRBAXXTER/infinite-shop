from django.test import TestCase
from UserApp.models import User


class TestUserModelStr(TestCase):
    def test_both_first_name_and_last_name_are_not_empty(self):
        user = User.objects.create(first_name='ahmad', last_name='ahmadi', phone='09121234567')
        self.assertEqual(str(user), 'ahmad ahmadi')

    def test_first_name_is_empty(self):
        user = User.objects.create(first_name='', last_name='ahmadi', phone='09121234567')
        self.assertEqual(str(user), '09121234567')

    def test_last_name_is_empty(self):
        user = User.objects.create(first_name='ahmad', last_name='', phone='09121234567')
        self.assertEqual(str(user), '09121234567')

    def test_both_first_name_and_last_name_are_empty(self):
        user = User.objects.create(first_name='', last_name='', phone='09121234567')
        self.assertEqual(str(user), '09121234567')
