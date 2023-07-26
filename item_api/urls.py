from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemView, SingleItemView

urlpatterns = [
     path('all/', ItemView.as_view(), name = 'all_items'),
     path('<slug:slug>', SingleItemView.as_view(), name = 'single_item')
]