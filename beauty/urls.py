from django.conf.urls.static import static
from django.urls import path

from beatycity import settings
from beauty import views

app_name = 'beauty'

urlpatterns = [
    path('', views.show_home, name='index'),
    path('notes/', views.show_notes, name='notes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
