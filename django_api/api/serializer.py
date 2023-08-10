from django.contrib import auth
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

import base64
import json
import pyotp

from .config import otp_config
from .models import User
from .send_email import send_otp


SECRET_DATA = otp_config()
SECRET_KEY = SECRET_DATA['secret']
SECRET_KEY_ENCODED = base64.b32encode(SECRET_KEY.encode()).decode()


class RestrictedAccessSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(max_length=68, min_length=3,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['password','username','tokens']


    def validate(self, attrs):
        user = self.authenticate_user(attrs)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        return True

    
    def main(self, attrs):
        user = self.authenticate_user(attrs)
        self.generate_otp(user)
        # send_otp(user)
        tokens = self.get_tokens(user)
        if settings.DEBUG == True:
            return {
            "refresh":str(tokens["refresh"]),
            "access": str(tokens["access"]),
            "otp": user.otp
            }
        else:
            return {
                "refresh":str(tokens["refresh"]),
                "access": str(tokens["access"])
                }


    def generate_otp(self, user):
        totp = pyotp.TOTP(SECRET_KEY_ENCODED, interval=6000)
        totp.now()
        user.otp = f'{totp.now()}'
        user.save()


    @classmethod
    def get_tokens(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['scope'] = 'restricted'
        return {
            "refresh":token,
            "access": token.access_token
        }
    

    @classmethod
    def authenticate_user(cls, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        return user



class FullAccessSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['scope'] = 'full'

        return token
    

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


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(label=("OTP"),max_length=6, min_length=6)
    auth = serializers.CharField()
    # auth = serializers.DictField()


    # With the token and otp validate
    def validate(self, data):
        otp = data['otp']
        token = data['auth']
        token = token.split(' ')[-1]

        access_token = AccessToken(token)
        payload_data = access_token.payload
        user = User.objects.get(id=payload_data['user_id'])

        validated_otp = User.objects.filter(username=user.username, otp=otp)
        if not validated_otp:
            msg = ('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        full_tokens = FullAccessSerializer()
        tokens = full_tokens.get_token(user)
        auth = json.dumps({
                "access": str(tokens.access_token),
                "refresh": str(tokens)
        })
        # auth = 1
       
        return {
            "otp": "",
            "auth": auth
        }
