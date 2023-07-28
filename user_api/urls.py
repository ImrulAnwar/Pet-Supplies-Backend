from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name='register'),
    path('superregister', views.SuperUserRegister.as_view(), name='super_register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('', views.UserView.as_view(), name='user'),
    path('activate/', include('verification_api.urls')),
]
