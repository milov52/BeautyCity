from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, SMSCode


@admin.register(SMSCode)
class SMSCodeAdmin(admin.ModelAdmin):
    search_fields = ['number', 'client__phone_number']
    list_display = ['number', 'client']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {
            'fields': (
                'phone_number',
                'username',
                'photo',
                'is_manager',
                'first_name',
                'last_name',
            )
        }),
    )

    list_display = ['id', 'phone_number', 'first_name', 'photo']
    search_fields = ['phone_number', 'username']
