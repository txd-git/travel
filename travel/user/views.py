import random

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from tools.sms import YunTongXin
from .models import UserProfile
import json
import hashlib
from tools.token import make_token
from django.core.cache import cache
from tools.random_word import random_word


# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        password = json_obj['password']
        try:
            user = UserProfile.objects.get(username=username)
        except Exception as e:
            print('error is %s' % e)
            return JsonResponse({'code': 1007, 'error': 'name is worng'})
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_t = md5.hexdigest()
        if password_t != user.password:
            return JsonResponse({'code': 1009, 'error': 'password is worng'})
        token = make_token(username)
        return JsonResponse({'code': 200, 'username': username, 'data': {'token': token.decode()}})


def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        email = json_obj['email']
        phone = json_obj['phone']
        ver_code = json_obj['ver_code']
        print(ver_code)

        # 校验验证码
        cache_ver_key = 'ver'
        old_ver_code = cache.get(cache_ver_key)
        print(old_ver_code)
        if not old_ver_code:
            result = {'code': 1015, 'error': '验证码错误！'}
            return JsonResponse(result)
        if str(ver_code) != old_ver_code:
            result = {'code': 1016, 'error': '验证码错误！'}
            return JsonResponse(result)

        # 校验全部信息都已填写
        if len(username) > 30 or username == "":
            result = {'code': 1001, 'error': 'name is worng'}
            return JsonResponse(result)
        if not email:
            result = {'code': 1002, 'error': 'email is worng'}
            return JsonResponse(result)
        if not phone:
            result = {'code': 1003, 'error': 'phone is worng'}
            return JsonResponse(result)

        if not password_1 and not password_2:
            result = {'code': 1004, 'error': 'password is null'}
            return JsonResponse(result)

        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 1005, 'error': 'name is worng'}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {'code': 1006, 'error': 'password is worng'}
            return JsonResponse(result)

        md5 = hashlib.md5()
        md5.update(password_1.encode())
        password_m = md5.hexdigest()

        # 存数据
        try:
            user = UserProfile.objects.create(username=username, password=password_m, email=email, phone=phone,nickname=username)
        except Exception as e:
            print('error is %s' % e)
            result = {'code': 1007, 'error': 'username is worng'}
            return JsonResponse(result)
        token = make_token(username)
        # return HttpResponse("--nihao post--")
        return JsonResponse({'code': 200, 'username': username, 'data': {'token': token.decode()}})


def ver_code(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    word = json_obj['word']
    if word == 'ok':
        list01 = []
        random_word(6, list01)
        words = ''.join(list01)
        print(words)
        chache__key = 'ver'
        cache.set(chache__key, words, 60)
        return JsonResponse({'code': 200, 'verifte': words})
    else:
        return JsonResponse({'code': 1019, 'erorr': '获取验证码失败!'})
