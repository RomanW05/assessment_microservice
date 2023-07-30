from django.contrib import auth

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.settings import SIMPLE_JWT

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

import base64
import json
import pyotp
import random

from .config import otp_config
from .models import User
from .send_email import send_otp

# print(SIMPLE_JWT)
SECRET_DATA = otp_config()
SECRET_KEY = SECRET_DATA['secret']
SECRET_KEY_ENCODED = base64.b32encode(SECRET_KEY.encode()).decode()


    





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
 
        return {
            'refresh': data['tokens']()['refresh'],
            'access': data['tokens']()['access']
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
        print(user.otp)
        # send_otp(otp, user.email)
 
        # return user
        return {
            'otp': user.otp,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
    
    @classmethod
    def get_token(cls, user):
        print('classmethod')
        token = super().get_token(user)

        # Add custom claims
        token['scope'] = 'Full'

        return token
    

















class RestrictedAccessSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(max_length=68, min_length=3,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['password','username','tokens']


    def validate(self, attrs):
        print('validating\n')
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
        print(user.get_username(), 'user\n')
        tokens = self.get_tokens(user)
        return {
            'otp': user.otp,
            'email': user.email,
            'username': user.username,
            'access': str(tokens['access']),
            'refresh': str(tokens['refresh']),
        }
    
    @classmethod
    def get_tokens(cls, user):
        token = super().get_token(user)
        print(token.token_type, 'override get tokens restricted serializer\n')

        # Add custom claims
        token['scope'] = 'restricted'

        return {
            "refresh":token,
            "access": token.access_token
        }



































class FullAccessSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['scope'] = 'Full'

        return token
    


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
    token = serializers.SerializerMethodField()

    def validate(self, attrs):
        token = attrs.headers["Authorization"]
        otp = attrs.data["otp"]
        # strip = settings.SIMPLE_JWT['AUTH_HEADER_TYPES']
        token = token[7:]
        access_token = AccessToken(token)
        payload_data = access_token.payload
        print(payload_data, 'payload_data')
        print(payload_data['user_id'], 'payload_data.user_id')
        user = User.objects.get(pk=payload_data['user_id'])
        username = User.objects.get(username=user)
        validated_otp = User.objects.filter(username=username, otp=otp).select_related("user").first()
        
        if not validated_otp:
            msg = ('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "user_id" and "otp".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = validated_otp.user
        return attrs
    

        if str(user.otp)==otp:
            user.verified = True
            user.save()
            return True
        else:
            return False


        # user_id = 
        auth_ = attrs.get.headers['Authentication']
        user_id = attrs.get('user_id')
        otp = attrs.get('otp')

        if user_id and otp:

            validated_otp = Otp.objects.filter(user_id=user_id, otp=otp).select_related("user").first()

            if not validated_otp:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "user_id" and "otp".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = validated_otp.user
        return attrs