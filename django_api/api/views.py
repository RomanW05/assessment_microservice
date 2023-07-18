from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication, JWTAuthentication

from django.views.generic.base import TemplateView

from .serializer import RegisterSerializer, LoginSerializer
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import BlacklistMixin



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


class Dashboard(generics.ListCreateAPIView):
    template_name = "dashboard.html"
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return render(request, self.template_name)  
    

class Logout(APIView):
    authentication_classes = [JWTStatelessUserAuthentication]

    def post(self, request):
        print('Logging out')
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            user , token = response
            print(BlacklistMixin.check_blacklist('token'))
            # rest_framework_simplejwt.exceptions.TokenError: Token is blacklisted
            try:
                reply = BlacklistMixin.blacklist(token)
                print('before verify')
                
                # print('verifying2')
                if reply[1]:
                    print('DONE')
                    return HttpResponseRedirect('/login', status=status.HTTP_200_OK)
                else:
                    print('Token not blacklisted')
                    return Response(status=status.HTTP_204_NO_CONTENT) 

            except Exception as e:
                print(e)
                
        else:
            print("no token is provided in the header or the header is missing")

        return Response(status=status.HTTP_204_NO_CONTENT)



class redirect(APIView):
    template_name = "dashboard3.html"
    
    def get(self, request):
        return render(request, self.template_name, None)  

