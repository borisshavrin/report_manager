from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=256, verbose_name='Имя пользователя', unique=True)
    image = models.ImageField(upload_to='users_images', blank=True)
    image_url = models.URLField(blank=True)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=256, verbose_name='Отчество', blank=True)
    position = models.CharField(max_length=256, verbose_name='Должность', blank=True)
    stuff_number = models.CharField(max_length=256, verbose_name='Табельный номер')
