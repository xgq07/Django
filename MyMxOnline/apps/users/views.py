# users/views.py

from django.shortcuts import render
from django.contrib.auth import authenticate,login

from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,UploadImageForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_eamil
from django.contrib.auth.mixins  import  LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.core.urlresolvers import reverse
from .models import Banner
from courses.models import Course

#邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    '''用户登录'''

    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):

            # 如果不是null说明验证成功
            if user is not None:
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活', 'login_form': login_form})
            # 只有当用户名或密码不存在时，才返回错误信息到前端
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})

        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,'login.html',{'login_form':login_form})


# 激活用户
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
         # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request,'active_fail.html')
        # 激活成功跳转到登录页面
        return render(request, "login.html", )


class RegisterView(View):
    '''用户注册'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email = user_name):
                return render(request, 'register.html', {'register_form':register_form,'msg': '用户已存在'})

            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


class ForgetPwdView(View):
    '''找回密码'''
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email',None)
            send_register_eamil(email,'forget')
            return render(request, 'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

class ResetView(View):
    '''重置密码'''
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form })


class UserinfoView(LoginRequiredMixin,View):
    '''用户个人信息'''
    def get(self,request):
        return render(request,'usercenter-info.html',{})

class UploadImageView(LoginRequiredMixin,View):
    '''用户图像修改'''
    def post(self,request):
        #上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        # image_form = UploadImageForm(request.POST,request.FILES)
        # if image_form.is_valid():
        #     image = image_form.cleaned_data['image']
        #     request.user.image = image
        #     request.user.save()
        #     return HttpResponse('{"status":"success"}', content_type='application/json')
        # else:
        #     return HttpResponse('{"status":"fail"}', content_type='application/json')
        #另一方法
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',  content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class IndexView(View):
    '''首页'''
    def get(self,request):
        #轮播图
        all_banners = Banner.objects.all().order_by('index')
        #课程
        courses = Course.objects.filter(is_banner=False)[:6]
        #轮播课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        #课程机构
        course_orgs = Course.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
        })