from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'user'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    role = models.CharField(max_length=100, choices=ROLES, default='user')

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['first_name', 'email']),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
