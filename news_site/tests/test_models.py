from news.models import User
from django.test import TestCase


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='xx@gmail.com', password='xx')

    def test_email(self):
        user = User.objects.get(id=1)
        #email = user._meta.get_field('email').verbose_name
        self.assertEquals(user.email, 'xx@gmail.com')

    def test_length_password(self):
        max_length = self.user




#class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         """
#         вызывается каждый раз перед запуском теста на уровне настройки всего класса. 
#         Вы должны использовать данный метод для создания объектов, 
#         которые не будут модифицироваться/изменяться в каком-либо из тестовых методов.
#         """
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         """ 
#         вызывается перед каждой тестовой функцией для настройки объектов, 
#         которые могут изменяться во время тестов (каждая функция тестирования будет получать "свежую" версию данных объектов) 
#         """
#         print("setUp: Run once for every test method to setup clean data.")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)