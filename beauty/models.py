from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'


class ServiceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'


class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    photo = models.ImageField(upload_to='service_photos/')
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Master(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=255)
    rating = models.IntegerField(null=True)     # Needs to automatically calculate
    experience = models.DurationField()
    photo = models.ImageField(upload_to='service_photos/')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number_of_stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ConsultationRequest(models.Model):
    # The following two fields are filled in automatically if the user exists
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(region='RU')
    question = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заявка на консультацию'
        verbose_name_plural = 'Заявки на консультации'


class AvailableDateTime(models.Model):
    datetime = models.DateTimeField()

    def __str__(self):
        return self.datetime

    class Meta:
        verbose_name = 'Доступные дата и время'
        verbose_name_plural = 'Доступные даты'


class ServiceSignUp(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    master = models.ForeignKey(Master, on_delete=models.PROTECT)
    price = models.IntegerField()
    datetime = models.OneToOneField(AvailableDateTime, on_delete=models.PROTECT)
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT)
    paid = models.BooleanField(default=False)
    tips = models.IntegerField()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Payment(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
