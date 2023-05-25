from django.contrib import admin
from .models import (
    Salon,
    Service,
    Master,
    Review,
    ConsultationRequest,
    AvailableDateTime,
    ServiceSignUp,
)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address']
    list_display = ['name', 'address']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'salon']
    list_display = ['name', 'price', 'salon']
    list_filter = ['price']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'salon']
    list_display = [
        'first_name',
        'last_name',
        'specialty',
        'salon',
        'formatted_experience',
    ]
    list_filter = ['specialty', 'rating']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['user', 'text']
    list_display = ['user', 'number_of_stars', 'created_at', 'updated_at']
    list_filter = ['number_of_stars']


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone', 'user']
    list_display = ['name', 'phone', 'user']


@admin.register(AvailableDateTime)
class AvailableDateTimeAdmin(admin.ModelAdmin):
    search_fields = ['datetime']
    list_display = ['datetime']


@admin.register(ServiceSignUp)
class ServiceSignUpTimeAdmin(admin.ModelAdmin):
    search_fields = ['phone', 'name']
    list_display = ['phone', 'service', 'master', 'salon', 'datetime']
