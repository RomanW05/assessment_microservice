from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
# from rest_framework_simplejwt.views import TokenBlacklistView



app_name = 'api'


urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('register/', views.Register.as_view(), name="register"),
    path('verify_otp/', views.verifyOTPView.as_view(), name='verify otp'),

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
]