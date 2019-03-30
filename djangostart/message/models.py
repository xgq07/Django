from django.db import models

# Create your models here.
class UserMessage(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'用户名')
    message = models.CharField(max_length=500,verbose_name=u'留言信息')

    class Meta:
        verbose_name = u'用户留言信息'
       