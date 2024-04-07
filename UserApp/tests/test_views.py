from django.test import TestCase, Client
from django.urls import reverse
from UserApp.views import *


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_view_GET(self):
        response = self.client.get(reverse('UserApp:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.failUnless(response.context['form'], UserRegisterForm)

    def test_user_register_view_POST_form_valid(self):
        response = self.client.post(reverse('UserApp:register'),
                                    {'first_name': 'احمد',
                                     'last_name': 'احمدی',
                                     'phone': '09125866779',
                                     'password': 'Test@123456',
                                     'password2': 'Test@123456'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('IndexApp:index'))
        self.assertEqual(User.objects.filter(phone='09125866779').exists(), True)

    def test_user_register_view_POST_form_invalid(self):
        response = self.client.post(reverse('UserApp:register'),
                                    {'first_name': 'احمد',
                                     'last_name': 'احمدی',
                                     'phone': '09125866779',
                                     'password': 'test@123456',
                                     'password2': 'test@12345'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.failUnless(response.context['form'], UserRegisterForm)
        self.assertFormError(response.context['form'], 'password2', 'رمز عبور ها متفاوت هستند.')
