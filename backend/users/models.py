from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import EMAIL_LENGTH, MAX_FIO_LENGTH, USERNAME_LENGTH
from core.validators import username_validator


class User(AbstractUser):
    email = models.EmailField('Почта', unique=True, max_length=EMAIL_LENGTH)
    username = models.CharField(
        'Никнейм',
        unique=True,
        validators=(username_validator,),
        max_length=USERNAME_LENGTH
    )
    first_name = models.CharField('Имя', max_length=MAX_FIO_LENGTH)
    last_name = models.CharField('Фамилия', max_length=MAX_FIO_LENGTH)
    avatar = models.ImageField(
        'Аватар',
        upload_to='users/avatars/',
        blank=True,
        null=True
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_subscription'
            )
        ]
