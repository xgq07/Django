from organization.views import OrgView,AddUserAskView,OrgHomeView
from django.conf.urls import url,include
#from django.urls import path,re_path

# 要写上app的名字
app_name = "organization"

urlpatterns = [
    #课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home")
]