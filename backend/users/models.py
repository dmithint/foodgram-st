from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        unique=True
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254
    )

    REQUIRED_FIELDS = [
        'username',
        'password',
        'first_name',
        'last_name',
    ]

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.username}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор, на которого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_user_author'
            )]
