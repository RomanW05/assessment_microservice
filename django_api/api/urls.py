from . import views
from django.urls import path


app_name = 'api'

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('register/', views.Register.as_view(), name="register"),
    path('verify_otp/', views.verifyOTP.as_view(), name='verify otp'),

    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
]