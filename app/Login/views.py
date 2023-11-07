
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required



# 登录模块
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return JsonResponse({"status": "ok"})
    return JsonResponse({"message": "no login"}, status=401)


# 注册用户
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "User already exists"}, status=400)

        else:
            User.objects.create_user(username=username, password=password)
            return JsonResponse({"status": "ok"})
    return JsonResponse({"message": "please register"})


# 登出模块
def logout(request):
    auth.logout(request)
    return JsonResponse({"status": "ok"})


@login_required(login_url='/api/auth/login')
def check_auth(request):
    return JsonResponse({"auth": "ok"})

