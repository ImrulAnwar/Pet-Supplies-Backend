from django.urls import path
from . import views

urlpatterns = [
    path('email/<str:email_token>', views.EmailActivationView.as_view(),
         name='activate_email'),
    path('email', views.SendEmailView.as_view(), name='send_email'),
]
