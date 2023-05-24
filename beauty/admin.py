from django.contrib import admin
from .models import Salon, ServiceType, Service, Master, Review, ConsultationRequest, AvailableDateTime, ServiceSignUp

admin.site.register(Salon)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Master)
admin.site.register(Review)
admin.site.register(ConsultationRequest)
admin.site.register(AvailableDateTime)
admin.site.register(ServiceSignUp)
