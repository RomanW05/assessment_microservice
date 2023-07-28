from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenBlacklistView





app_name = 'api'


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.Register.as_view(), name="register"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),

    # path('loggedin/', views.loggedin.as_view(), name="is logged in"),
    path('redirect/', views.redirect.as_view(), name='redirect'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('verify_otp/', views.verifyOTPView.as_view(), name='verify_otp'),
    path('analyzetoken/', views.analyzeToken.as_view(), name='analyzetoken'),

    # path('totp/create', views.TOTPCreateView.as_view(), name='totp-create'),
    # path(r'totp/login/(?P<token>[0-9]{6})/', views.TOTPVerifyView.as_view(), name='totp-login'),
]