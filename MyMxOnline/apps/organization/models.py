from datetime import datetime

from django.db import models

# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    ORG_CHOICES = (
        ("pxjg", u"培训机构"),
        ("gx", u"高校"),
        ("gr", u"个人"),
    )
    name = models.CharField('机构名称',max_length=50)
    desc = models.TextField('机构描述')
    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name=u"机构类别", default="pxjg")
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    image = models.ImageField('logo',upload_to='org/%Y%m',max_length=100)
    address = models.CharField('机构地址',max_length=150,)
    city = models.ForeignKey(CityDict,verbose_name='所在城市',on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now)
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    tag = models.CharField('机构标签',max_length=10,default='全国知名')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(default= '',upload_to="teacher/%Y/%m",verbose_name="头像",max_length=100)
    teacher_age = models.IntegerField('年龄', default=25)

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name