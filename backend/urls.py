from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', include("item_api.urls")),
    path('user/', include('api.urls')),
]
