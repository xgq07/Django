#coding=utf-8
from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    '''注册验证表单'''  
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    # 验证码
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})