from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ActivateEmailSerializer, SendEmailSerializer


class EmailActivationView(APIView):
    def post(self, request, *args, **kwargs):
        email_token = kwargs.get('email_token')
        serializer = ActivateEmailSerializer(
            data=request.data, context={'request': request, 'email_token': email_token})
        if serializer.is_valid():
            return Response({"message": "Your Email is Activated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendEmailSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"message": "Activation email sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
