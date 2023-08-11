from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication
from rest_framework_simplejwt.tokens import BlacklistMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .authentication import HasRestrictedScope, HasFullScope, IsWhitelisted
from .serializer import RegisterSerializer, RestrictedAccessSerializer, OTPSerializer, DeleteUserSerializer


# Access views
class DeleteAccount(generics.ListCreateAPIView):
    serializer_class = DeleteUserSerializer
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated, HasFullScope, IsWhitelisted]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class Register(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


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

        return Response(data, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class verifyOTP(APIView):
    serializer_class = OTPSerializer
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated, HasRestrictedScope, IsWhitelisted]

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if not request.data["otp"]:
            return Response({'Error':'OTP missing'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data={'otp':request.data["otp"], 'auth':request.headers['Authorization']})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class Logout(generics.GenericAPIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated, HasFullScope, IsWhitelisted]

    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is None:
            raise BaseException
        else:
            user, token = response

        response = BlacklistMixin.blacklist(token)
        if response[1] == True:  # Token added to blacklist
            print('token blacklisted')
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            print('token not blacklisted')
            return Response(status=status.HTTP_304_NOT_MODIFIED)


# Data views
class Dashboard(generics.GenericAPIView):
    template_name = "dashboard.html"
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated, HasFullScope, IsWhitelisted]

    def get(self, request):
        return render(request, self.template_name, None, status=status.HTTP_200_OK)

