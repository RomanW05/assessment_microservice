from django.urls import path
from . import views


urlpatterns = [
    path('login', views.index, name='Login'),
    path('register/', views.register, name='Register'),
    path('hello/', views.HelloView.as_view(), name ='hello'),
]

