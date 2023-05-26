from django.conf.urls.static import static
from django.urls import path

from beatycity import settings
from beauty import views

app_name = 'beauty'

urlpatterns = [
    path('', views.show_home, name='index'),
    path('notes/', views.show_notes, name='notes'),
    path('service-finally/', views.show_service_finally, name='service-finally'),
    path('service/', views.show_service, name='service'),
    path('manager/', views.show_manager_page, name='manager'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('make_payment/<int:order_id>', views.make_payment_by_id, name='make_payment'),
    # path('make_payment/', views.make_payment, name='make_payment'),
    path('update_payment_status', views.update_payment_status, name='update_payment_status')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
