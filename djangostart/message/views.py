from django.shortcuts import render
from message.models import UserMessage
from django.views.decorators import csrf
# Create your views here.
def getform(request):
    message = None
    all_messages = UserMessage.objects.filter(name='xgq')
    if all_messages:
        message = all_messages[0]
    

    # 查询
    # all_messages = UserMessage.objects.all()
    # for message in all_messages:
    #     print(message.name)
    # 从post请求里的htmlGet元素并保存
    # if request.POST:
    #     name = request.POST.get('name','')
    #     message = request.POST.get('message','')

    #     _usermess = UserMessage()
    #     _usermess.name = name
    #     _usermess.message = message
    #     _usermess.save()

    return render(request,'message_form.html',
        {"my_message":message}
    )