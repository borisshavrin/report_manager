from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)
    image_url = models.URLField(blank=True)


class UserProfile(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    lastname = models.CharField(max_length=256, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=256, verbose_name='Отчество')
    position = models.CharField(max_length=256, verbose_name='Должность')
    stuff_number = models.CharField(max_length=256, verbose_name='Табельный номер')

    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOISE = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(
        User,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )

    about_me = models.TextField(
        verbose_name='О себе',
        max_length=512,
        blank=True,
    )

    gender = models.CharField(
        verbose_name='Пол',
        max_length=1,
        choices=GENDER_CHOISE,
        blank=True,
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
