from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='salon_photos/')

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
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Master(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    rating = models.IntegerField(null=True)     # Needs to automatically calculate
    experience = models.DurationField()
    photo = models.ImageField(upload_to='master_photos/')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def formatted_experience(self):
        total_months = self.experience.days // 30
        years = total_months // 12
        months = total_months % 12
        return f'{years}г. {months} мес.'

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number_of_stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ConsultationRequest(models.Model):
    # The following two fields are filled in automatically if the user exists
    name = models.CharField(max_length=255)
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
        return str(self.datetime)

    class Meta:
        verbose_name = 'Доступные дата и время'
        verbose_name_plural = 'Доступные даты'


class ServiceSignUp(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    master = models.ForeignKey(Master, on_delete=models.PROTECT)
    datetime = models.OneToOneField(AvailableDateTime, on_delete=models.PROTECT)
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT)
    payment_id = models.CharField(verbose_name="Айди платежа", max_length=100, blank=True)
    paid = models.BooleanField(default=False)
    tips = models.IntegerField()
    # The following two fields are filled in automatically if the user exists
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(region='RU')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    question = models.TextField(blank=True)

    def __str__(self):
        return f'Запись {self.user.username} на {self.service.name}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
