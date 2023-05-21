from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(verbose_name='Телефон', max_length=30)

    def __str__(self):
        return self.username
