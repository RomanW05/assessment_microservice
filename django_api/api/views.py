from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication, JWTAuthentication
from rest_framework_simplejwt.tokens import BlacklistMixin

from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .authentication import HasRestrictedScope
from .models import User
from .serializer import RegisterSerializer, LoginSerializer, LogoutSerializer, CustomTokenObtainPairSerializer




class Register(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    # queryset = User.objects.all()

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user_data = serializer.data
        return Response(status=status.HTTP_201_CREATED)


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # serializer_class = CustomTokenObtainPairSerializer
    template_login = "login.html"
    template_validate = "validate.html"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validate(attrs={
            'username': request.data['username'],
            'password': request.data['password']
            })

        print(data['otp'])

        # user = authenticate(request, username=request.data['username'], password=request.data['password'])
        
        # next_route_url = reverse('/api/verify_otp') + f"?username={request.data['username']}"
        # return HttpResponseRedirect(f"/api/verify_otp/{request.data['username']}")
        
        # return HttpResponseRedirect('/api/verify_otp', username=request.data['username'])
        # return HttpResponseRedirect()
        
        # return render(request, status=status.HTTP_202_ACCEPTED)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
    


class Dashboard(generics.GenericAPIView):
    template_name = "delete.html"
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [HasRestrictedScope]
    
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
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]
    template_name = "dashboard3.html"
    
    def get(self, request):
        return render(request, self.template_name, None)  





from rest_framework_simplejwt.tokens import AccessToken, Token


class verifyOTPView(APIView):
    serializer_class = CustomTokenObtainPairSerializer
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        token = request.headers["Authorization"]
        otp = request.data["otp"]

        token = token[7:]
        access_token = AccessToken(token)
        payload_data = access_token.payload
        print(payload_data, 'payload_data')
        print(payload_data['user_id'], 'payload_data.user_id')

        user = User.objects.get(pk=payload_data['user_id'])

        # username = payload_data.get('username')
        print(user, 'username')

        user = User.objects.get(username=user)
        print(user.otp, 'user.otp')
        if str(user.otp)==otp:
            user.verified = True
            user.save()
            return Response("Verification Successful")
        
        else:
            return Response("Verification Failed")



class analyzeToken(APIView):


    def get(self, request):
        print(request.auth, 'request.auth')
        token = request.headers["Authorization"]
        token = token[7:]
        access_token = AccessToken(token)
        print(request.auth.payload, 'request.auth.payload')
        print(access_token, 'access_token')
        payload_data = access_token.payload
        print(payload_data, 'payload_data')
        print(payload_data['user_id'], 'payload_data.user_id')
        return Response("Checked") 


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer