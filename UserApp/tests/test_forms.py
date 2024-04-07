from django.test import TestCase
from UserApp.forms import *
from UserApp.models import User


class TestUserRegisterForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            first_name='amir',
            last_name='baxxter',
            phone='09123456789',
            password='test123'
        )

    def test_form_is_valid(self):
        form = UserRegisterForm(data={
            'first_name': 'رضا',
            'last_name': 'حمیدی',
            'phone': '09123456788',
            'password': 'test@12345',
            'password2': 'test@12345'
        })
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid(self):
        form = UserRegisterForm(data={
            'first_name': 'amir',
            'last_name': 'baxxter',
            'phone': '09123456789',
            'password': 'test123',
            'password2': 'test1234'
        })
        self.assertFalse(form.is_valid())

    def test_empty_form(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_exist_phone(self):
        form = UserRegisterForm(data={
            'first_name': 'amir',
            'last_name': 'baxxter',
            'phone': '09123456789',
            'password': 'test123',
            'password2': 'test123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'], ['شماره ی تماس تکراری است.'])

    def test_different_password(self):
        form = UserRegisterForm(data={
            'first_name': 'amir',
            'last_name': 'baxxter',
            'phono': '09123456789',
            'password': 'test@1234',
            'password2': 'test@12345'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['رمز عبور ها متفاوت هستند.'])
