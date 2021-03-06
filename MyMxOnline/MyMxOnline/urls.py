"""MyMxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
#from extra_apps import xadmin as xadmin
import xadmin
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,IndexView
from organization.views import OrgView
from django.views.static import serve
from MyMxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',IndexView.as_view(),name="index"),
    url('^login/$',LoginView.as_view(),name="login"),
    url('^register/$',RegisterView.as_view(),name='register'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active'),
    url(r'^forget/$',ForgetPwdView.as_view(),name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    #课程机构url配置
    url(r'^org/', include(('organization.urls','organization'), namespace="org")),
    # url(r'^org_list/$',OrgView.as_view(),name = 'org_list'),
    url(r"course/", include(('courses.urls','course'), namespace="course")),  #include中是模块名
    #个人信息
    url(r"^users/", include(('users.urls','users'), namespace="users")),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),
]