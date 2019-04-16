from django.conf.urls import url,include
from .views import UserinfoView,UploadImageView,UpdatePwdView

app_name = 'users'

urlpatterns = [
    #用户信息
    url(r"^info/", UserinfoView.as_view(),name='user_info'),
    #用户图像上传
    url(r"^image/upload", UploadImageView.as_view(),name='image_upload'),
    #用户个人中心修改密码
    url("update/pwd/", UpdatePwdView.as_view(),name='update_pwd'),
]