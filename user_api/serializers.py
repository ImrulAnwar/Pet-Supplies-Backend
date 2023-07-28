from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
    # overridden

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(
            email=clean_data['email'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        return user_obj


class SuperUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
    # overridden

    def create(self, clean_data):
        user_obj = UserModel.objects.create_superuser(
            email=clean_data['email'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    # overridden
    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data['email'],
            password=clean_data['password']
        )

        if not user:
            raise ValidationError('user not found')
        # if not email verified or phone number verified raise ValidationError
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')


class ActivateEmailSerializer(serializers.Serializer):

    def validate(self, data, *args, **kwargs):
        # email = data.get('email')
        request = self.context.get('request')
        email = request.user.email
        email_token = self.context.get('email_token')
        # Get email_token from URL
        # print(str(email)+"\n"+str(email_token))
        user_obj = UserModel.objects.get(email=email, email_token=email_token)

        if user_obj:
            user_obj.is_email_verified = True
            user_obj.save()
        else:
            raise serializers.ValidationError(
                'Invalid email_token provided.')

        return data


class SendEmailSerializer(serializers.Serializer):

    def validate(self, data):
        request = self.context.get('request')
        email = request.user.email

        user_obj = UserModel.objects.get(
            email=email)
        if user_obj:
            email_token = user_obj.email_token
            self.send_account_activation_email(email, email_token)
        else:
            raise serializers.ValidationError(
                'Please login first and try again')
        return data

    def send_account_activation_email(self, email, email_token):
        subject = 'Verify your account!'
        email_from = settings.EMAIL_HOST_USER
        message = f'Click on the link to verify your account\n {settings.BASE_URL}/user/activate/email/{email_token}'
        send_mail(subject, message, email_from, [email])
