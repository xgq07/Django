from django.shortcuts import render
from django.views.generic.base import View

from .models import CourseOrg,CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class OrgView(View):
    '''课程机构'''

    def get(self, request):
        # 所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 有多少家机构
        org_nums = all_orgs.count()
        # 所有城市
        all_citys = CityDict.objects.all()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_orgs, 1, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
        })

