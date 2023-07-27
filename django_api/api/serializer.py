from rest_framework import serializers

from django.contrib import auth
# from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

import base64
import pyotp
import random

from .send_email import send_otp
from .config import otp_config
from .models import User


SECRET_DATA = otp_config()
SECRET_KEY = SECRET_DATA['secret']
SECRET_KEY_ENCODED = base64.b32encode(SECRET_KEY.encode()).decode()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=3,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['password','username','tokens']
        read_only_fields = ('id', 'verified')

    def get_tokens(self, obj):
        data = super().validate(obj)

        # Customize the response data with additional claims (scopes)
        data['scope'] = 'restricted'

        user = User.objects.get(username=obj['username'])
        # return data
        print(data['tokens']()['access'])
        return {
            'refresh': data['tokens']()['refresh'],
            'access': data['tokens']()['access']
        }
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        
        totp = pyotp.TOTP(SECRET_KEY_ENCODED, interval=6000)
        totp.now()
        user.otp = f'{totp.now()}'
        user.save()
        # send_otp(otp, user.email)
 
    
        return {
            'otp': user.otp,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            print(self.token, 'serializer')
            RefreshToken(token=self.token).blacklist()
        except TokenError:
            self.fail('bad_token')







class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('id', 'verified')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])

        totp = pyotp.TOTP(SECRET_KEY_ENCODED)
        totp.now()
        user.otp = totp.now()
        user.save()

        send_otp(user.otp, user.email)
        return user











class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, token):

        access_token = AccessToken(token)
        user = access_token.user
        token = super().get_token(user)

        # Customize the token payload with additional claims (scopes)
        # In this example, we set the scope to 'full'
        token['scope'] = 'full'

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Customize the response data with additional claims (scopes)
        data['scope'] = 'full'

        return data