from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication
from rest_framework_simplejwt.tokens import BlacklistMixin
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .authentication import HasRestrictedScope, HasFullScope
from .models import User
from .serializer import RegisterSerializer, LogoutSerializer, RestrictedAccessSerializer, OTPSerializer

from django_api import settings



class Register(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class Login(generics.ListCreateAPIView):
    serializer_class = RestrictedAccessSerializer
    template_login = "login.html"
    template_validate = "validate.html"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.main(attrs={
            'username': request.data['username'],
            'password': request.data['password']
            })

        return Response(data, status=status.HTTP_200_OK)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
    


class Dashboard(generics.GenericAPIView):
    template_name = "delete.html"
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [HasFullScope]
    
    def get(self, request):
        return render(request, self.template_name, None, status=status.HTTP_200_OK)



class Logout(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [HasFullScope]

    def post(self, request):
        try:
            print('serializer instantiation')
            serializer = self.serializer_class(data={'request':request})
            print('validating')
            serializer.is_valid(raise_exception=True)
            print('validation passed')
            serializer.blacklist(request.headers['Authorization'])
            return HttpResponseRedirect('/api/login', status=status.HTTP_308_PERMANENT_REDIRECT)
        except Exception as e:
            print('error:,', e)
            return Response({"error":str(e)}, status=status.HTTP_200_OK)
            # raise PermissionError
        





    


class verifyOTPView(APIView):
    serializer_class = OTPSerializer
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated, HasRestrictedScope]

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is None:
            raise BaseException

        serializer = self.serializer_class(data={'otp':request.data["otp"], 'auth':request.headers['Authorization']})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data['auth'], status=status.HTTP_200_OK)
        







class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = RestrictedAccessSerializer

