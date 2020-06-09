from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .other import uuid_gen


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)# date from datetime module
    permissions = (
            (1, '[ADMIN] - Can post without moderation, moderate posts'),
            (2, '[MODERATOR] - Can post without moderation'),
            (3, '[USER] - Can post with moderation')
        )
    uuid = models.CharField(max_length=40, default=uuid_gen(), unique=True)
    role = models.IntegerField(verbose_name='User role', default=3, choices=permissions)
    is_active = models.BooleanField(default=True)# banned or not
    is_admin = models.BooleanField(default=False)
    verification = models.BooleanField(default=False)#verification email
    objects = UserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = [] - при створенні суперюзера необов*язкові поля які будуть запитуватись(наприклад коли ми створюєвали суперюзера запитувало емеіл опціонально)

    def __str__(self):            
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, news_site):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = RichTextField()
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title}, {self.text}, {self.created}'

class ModerationPost(models.Model):
    title = models.CharField(max_length=200)
    text = RichTextField()
    created = models.DateTimeField(default=datetime.now)
    moderation_status = models.IntegerField()

    def __str__(self):
        return f'{self.moderation_status}'

class Comment(models.Model):
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}, {self.user}'

    


    

