from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    phone_number = PhoneNumberField(_('номер телефона'), unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
    photo = models.ImageField(
        blank=True,
        verbose_name='аватар',
        null=True
    )
    is_manager = models.BooleanField('является менеджером', default=False)
    def __str__(self):
        return str(self.phone_number)

class SMSCode(models.Model):
    number = models.CharField(
        'код',
        max_length=4,
        blank=True,
    )
    client = models.ForeignKey(
        User,
        related_name='code',
        verbose_name=_('клиент'),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('СМС код')
        verbose_name_plural = _('СМС коды')

    def __str__(self):
        return self.number