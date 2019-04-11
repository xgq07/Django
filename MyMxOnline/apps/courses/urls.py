from django.conf.urls import url,include
from .views import CourseListView

# 要写上app的名字
#app_name = "course"   

urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
]
