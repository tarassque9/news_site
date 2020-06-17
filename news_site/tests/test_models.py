from news.models import User
from django.test import TestCase


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='xx@gmail.com', password='xx')

    def test_email(self):
        user = User.objects.get(id=1)
        # email = user._meta.get_field('email').verbose_name
        self.assertEquals(user.email, 'xx@gmail.com')

    def test_length_password(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('password').max_length
        self.assertEquals(max_length, 100)
