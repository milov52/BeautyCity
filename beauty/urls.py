from django.conf.urls.static import static
from django.urls import path

from beatycity import settings
from beauty import views

app_name = 'storage'

urlpatterns = [
    path('', views.show_home, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
