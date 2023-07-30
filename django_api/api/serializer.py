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

        # Customize the response data with additional claims (scopes)
        # data['scope'] = 'restricted'
        print(data, 'data')
        # token = self.get_token(obj['username'])
        # print(token, 'token')

        # return data
        # print(data['tokens']()['access'])
        return {
            'refresh': data['tokens']()['refresh'],
            'access': data['tokens']()['access']
        }
    
        # user = User.objects.get(username=obj['username'])
        # return {
        #     'refresh': user.tokens()['refresh'],
        #     'access': user.tokens()['access']
        # }

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
        read_only_fields = ('id', 'verified')


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
 
        # return user
        print('validating success\n')
        tokens = self.get_token(user=user)
        # print(tokens, 'before returning')

        # print(tokens.access_tokens, 'tokens.access_tokens')
        # print(tokens['access'])
        # print( 'access token', tokens['access'], 'refresh token', tokens['refresh'])
        print('got tokens\n')
        token_access = tokens['access']
        token_refresh = tokens['refresh']
        print(token_access, token_refresh)
        return json.dumps(tokens)
        return {
            'otp': user.otp,
            'email': user.email,
            'username': user.username,
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(token.token_type)

        # Add custom claims
        token['scope'] = 'restricted'
        print(token.access_token.token_type, 'access token override get_token\n')
        # RefreshToken.access_token
        # RefreshToken.
        # return token
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