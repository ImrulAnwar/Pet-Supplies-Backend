from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemView, SingleItemView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all', ItemView.as_view(), name='all_items'),
    path('<slug:slug>', SingleItemView.as_view(), name='single_item')
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

