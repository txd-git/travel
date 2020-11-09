from django.http import JsonResponse
from django.shortcuts import render
from tools.logging_dec import logging_check
from user.models import UserProfile
import json
# Create your views here.




def change_user_info(request,username):
     if request.method=='GET':
         return render(request,'change_info.html')



@logging_check
def changeinfo(request,username):
    if request.method=='GET':
            try:
                user=UserProfile.objects.get(username=username)
                return JsonResponse({'code': 200, 'username': username,
                 'data': {'info': user.info, 'sign': user.sign, 'nickname': user.nickname,'avatar': str(user.avatar)}})
            except Exception as e:
                return JsonResponse({'code':1025,'error':'get wrong'})
    elif request.method=='PUT':
        json_str = request.body
        json_boj = json.loads(json_str)
        request.myuser.sign = json_boj['sign']
        request.myuser.nickname = json_boj['nickname']
        request.myuser.info = json_boj['info']
        request.myuser.save()
        result = {'code': 200, 'username': request.myuser.username}
        return JsonResponse(result)


@logging_check
def change_avatar(request,username):
    if request.method != 'POST':
        result = {'code': 10105, 'error': 'please give me POST'}
        return JsonResponse(result)
    # 从url中获取username
    # user = UserProfile.objects.get(username=username)
    # 从装饰器中由 request的附加属性myuser来获取user
    user = request.myuser
    user.avatar = request.FILES['avatar']
    user.save()
    # result={'code':200,'username':username}
    result = {'code': 200, 'username': user.username}
    return JsonResponse(result)