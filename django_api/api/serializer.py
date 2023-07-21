from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .send_email import send_otp
import random


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=68, min_length=6, write_only=True)
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

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
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['password','username','tokens']
        read_only_fields = ('id', 'verified')

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
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
        otp = random.randint(000000,999999)
        user.otp = otp
        user.save()
        # send_otp(otp, user.email)
 
    
        return {
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






class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['opt']


    def validate(self, attrs):
        user = User.objects.get(username=obj['username'])
        self.otp = attrs['otp']
        return attrs
    
    def save(self, **kwargs):
        try:
            print(self.token, 'serializer')
            RefreshToken(token=self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

