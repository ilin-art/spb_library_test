from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from events.managers import CustomUserManager


class CustomUser(AbstractUser):
    """Пользовательская модель пользователя."""
    phone_number = PhoneNumberField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="телефон"
    )
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='members',
        verbose_name="организация"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Organization(models.Model):
    """Модель организации."""
    title = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    address = models.CharField(max_length=255, verbose_name="адрес")
    postcode = models.CharField(max_length=10, verbose_name="почтовый индекс")

    def __str__(self):
        return self.title


class Event(models.Model):
    """Модель мероприятия."""
    title = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    organizations = models.ManyToManyField(
        'Organization',
        related_name='events',
        verbose_name="организации"
    )
    image = models.ImageField(
        upload_to='event_images/',
        null=True, blank=True,
        verbose_name="изображение"
    )
    participants = models.ManyToManyField(
        CustomUser,
        related_name='events_participated',
        blank=True,
        verbose_name="участники"
    )
    date = models.DateTimeField(verbose_name="дата")

    def __str__(self):
        return self.title
