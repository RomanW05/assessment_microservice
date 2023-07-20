from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication, JWTAuthentication
from rest_framework_simplejwt.tokens import BlacklistMixin
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .serializer import RegisterSerializer, LoginSerializer, LogoutSerializer


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
    template_name = "login.html"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class Dashboard(generics.GenericAPIView):
    template_name = "delete.html"
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            user , token = response
            try:
                BlacklistMixin.check_blacklist(token)
                # Valid token
                return render(request, self.template_name, None, status=status.HTTP_200_OK)

            except:
                # Error means token is not valid, pass and handle along with None response
                pass

        # Token is not valid
        return HttpResponseRedirect(redirect_to='/api/login', status=status.HTTP_307_TEMPORARY_REDIRECT)


class Logout(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)

        if response is not None:
            user , token = response
            try:
                result = BlacklistMixin.blacklist(token)
                if result[1]:
                    return HttpResponseRedirect('/api/login', status=status.HTTP_308_PERMANENT_REDIRECT)
                elif not result[1]:
                    return Response(status=status.HTTP_204_NO_CONTENT) 
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                print(e)

        return Response(status=status.HTTP_204_NO_CONTENT)




class redirect(APIView):
    template_name = "dashboard3.html"
    # authentication_classes = [JWTStatelessUserAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return render(request, self.template_name, None)  

