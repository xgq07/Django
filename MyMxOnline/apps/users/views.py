from django.shortcuts import render
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile
from forms import LoginForm


class CustomBackend(ModelBackend):
    def authenticate(self,username=None,password=None,**Kwargs):
        try:
            #user = UserProfile.objects.get(Q(username=username)|Q(email=username),Q(password=password))
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            #print(user)
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LoginView(View):
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")
            user = authenticate(username = user_name,password = pass_word)
            if user is not None:
                auth_login(request,user)
                return render(request,"index.html")
        else:
            return render(request,"login.html",{"msg":"用户名或密码错误!"})   

    def get(self,request):
        return render(request,"login.html",{"msg":"用户名或密码错误!"})

# Create your views here.

#基于函数的写法
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         user = authenticate(username = user_name,password = pass_word)
#         if user is not None:
#             auth_login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request,"login.html",{"msg":"用户名或密码错误!"})
#     elif request.method == "GET":
#         return render(request,"login.html",{})