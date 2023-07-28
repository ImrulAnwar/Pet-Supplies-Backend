from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError

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

    # overriden
    def validate(self, data, *args, **kwargs):
        try:
            request = self.context.get('request')
            email = request.user.email
            email_token = self.context.get('email_token')
            user_obj = UserModel.objects.get(
                email=email, email_token=email_token)
            user_obj.is_email_verified = True
            user_obj.save()
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('Invalid email_token provided.')
        except Exception as e:
            raise serializers.ValidationError(
                'Please login first and try again!')

        return data


class SendEmailSerializer(serializers.Serializer):

    # overriden
    def validate(self, data):
        try:
            request = self.context.get('request')
            email = request.user.email
            user_obj = UserModel.objects.get(email=email)
            email_token = user_obj.email_token
            self.send_account_activation_email(email, email_token)
        except Exception as e:
            raise serializers.ValidationError(
                'Please login first and try again!')
        return data

    def send_account_activation_email(self, email, email_token):
        subject = 'Verify your account!'
        email_from = settings.EMAIL_HOST_USER
        message = f'Click on the link to verify your account\n {settings.BASE_URL}/user/activate/email/{email_token}'
        try:
            send_mail(subject, message, email_from, [email])
        except BadHeaderError:
            raise serializers.ValidationError(
                'Invalid email header. Please try again later.')
        except Exception as e:
            raise serializers.ValidationError(
                'Failed to send activation email. Please try again later.')
