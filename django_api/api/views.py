from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .serializer import RegisterSerializer, LoginSerializer, LogoutSerializer, UserSerializer
from .models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken



class Register(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class Dashboard(APIView):
    template_name = "dashboard.html"
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return render(request, self.template_name, usernames=usernames)  
    
import base64
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
class Logout(APIView):

    serializer_class = LogoutSerializer
    authentication_classes = [JWTStatelessUserAuthentication]

    def post(self, request, format=None):
        print('Logging out')
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user , token = response
            print("this is decoded token claims", token.payload, f'User: {user}')
        else:
            print("no token is provided in the header or the header is missing")

        refresh = json.dumps(request.data)
        refresh = json.loads(refresh)
        # is_blacklisted = BlackListedToken()
        # token = RefreshToken(refresh["refresh"])
        # token.blacklist()
        # print(is_blacklisted.check(**refresh))
        # print(is_blacklisted, 'is blacklisted')

        # serializer = self.serializer_class(data=refresh)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # base64_token = base64.b64encode(bytes(refresh["refresh"], 'utf-8'))
        # encoded = RefreshToken(refresh["refresh"])
        token = request.data.get('refresh')
        print(token, 'TOKENM')
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        # print(encoded.blacklist())
        print('logged out')
        # return HttpResponseRedirect(redirect_to='/api/login')
        return Response(status=status.HTTP_204_NO_CONTENT)







class loggedin(APIView):
    authentication_classes = [JWTStatelessUserAuthentication]

    def get(self, request):
        
        status = self.request.user
        print(status, '<<<Status')

        if self.request.user.is_authenticated:
            usernames = [user.username for user in User.objects.all()]
            print(usernames)
            return Response(usernames)
        else:
            return Response("Not logged in")




class redirect(TemplateView):
    template_name = "dashboard3.html"
    
    def get(self, request):
        return render(request, self.template_name, None)  

