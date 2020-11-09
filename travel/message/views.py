from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from article.models import ArticlePost
from .models import Message
from tools.logging_dec import logging_check
import json


# Create your views here.
@logging_check
def send_message(request, id):
    if request.method != "POST":
        print("article_id")
        result = {"code": 10400, "error": "please uee POST"}
        return JsonResponse(result)
    json_obj = json.loads(request.body)
    try:
        content = json_obj['content']
    except Exception as e:
        return HttpResponse('**')
    p_id = json_obj.get('m_id', 0)
    try:
        article = ArticlePost.objects.get(id=id)
    except Exception as e:
        result = {'code': 1040, 'error': 'topic id error'}
        return JsonResponse(result)
    user = request.myuser
    Message.objects.create(article=article, content=content,
                           user=user,
                           p_id=p_id)
    return JsonResponse({'code': 200, "content": content})
