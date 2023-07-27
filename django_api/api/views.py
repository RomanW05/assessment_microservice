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

from .authentication import RestrictedScopePermission
from .models import User
from .serializer import RegisterSerializer, LoginSerializer, LogoutSerializer, CustomTokenObtainPairSerializer




# def get_user_totp_device(self, user, confirmed=None):
#     devices = devices_for_user(user, confirmed=confirmed)
#     for device in devices:
#         if isinstance(device, TOTPDevice):
#             return device

# class TOTPCreateView(APIView):
#     """
#     Use this endpoint to set up a new TOTP device
#     """
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, format=None):
#         user = request.user
#         device = get_user_totp_device(self, user)
#         if not device:
#             device = user.totpdevice_set.create(confirmed=False)
#         url = device.config_url
#         return Response(url, status=status.HTTP_201_CREATED)

# class TOTPVerifyView(APIView):
#     """
#     Use this endpoint to verify/enable a TOTP device
#     """
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, token, format=None):
#         user = request.user
#         device = get_user_totp_device(self, user)
#         if not device == None and device.verify_token(token):
#             if not device.confirmed:
#                 device.confirmed = True
#                 device.save()
#             return Response(True, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
# class VeriyOTP(APIView):
#     serializer_class = OTPSerializer

#     def post(self, request):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         serializer.is_valid(raise_exception=True)


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
    



# class verifyOTPView(APIView):
#     permission_classes = [RestrictedScopePermission]

#     def post(self, request):
#         username = request.data["username"]
#         otp = int(request.data["otp"])
#         user = User.objects.get(username=username)
#         if int(user.otp)==otp:
#             user.verified = True
#             #user.otp.delete()  #?? How to handle the otp, Should I set it to null??
#             user.save()
#             return Response("Verification Successful")
#         else:
#             raise Exception('Not verified')
#             raise PermissionDenied("OTP Verification failed")
        



    
# class VerifyOTP(APIView):
#     serializer_class = OTPSerializer
#     permission_classes = [IsAuthenticatedWithUser]

#     def get(self, request):
#         user = request.user
#         return Response({"message": f"Hello, {user.username}!"}, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # permission_classes = [IsAuthenticated]
#         return Response(status=status.HTTP_200_OK)

# class TwoFactorAuth(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]


class Dashboard(generics.GenericAPIView):
    template_name = "delete.html"
    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated, RestrictedScopePermission]
    # permission_classes = [RestrictedScopePermission]
    
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