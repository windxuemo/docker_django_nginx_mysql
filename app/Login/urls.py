
from django.urls import path
from .views import login, register, logout, check_auth

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('check-auth/', check_auth, name='check')
]

