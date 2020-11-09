import json
import time
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
from customized.models import CityInfo
from tq.models import City
from tools.view_cache import cache_dec
from tools.get_address import get_addree
from tools.get_weather import get_weather
from .models import CityInfo


# 获取传输过来的地址
# def get_addree(position):
#     print(position)
#     address={}
#     for i in range(len(position)):
#         if position[i] == '省':
#             for s in range(i, len(position)):
#                 if position[s] == '市':
#                     shi = position[i + 1:s]
#                     address['shi']=shi
#                     for q in range(s, len(position)):
#                         if position[q] == '区' or position[q] == '县':
#                             qu = position[s + 1:q]
#                             address['qu'] = qu
#
#     if not address:
#         address['shi']=position
#         address['qu']=position
#     return address

# 获取景点天气
# def get_weather(position):
#     # print(position)
#     try:
#         city = City.objects.get(city_name=position)
#         # print(city.number)
#     except Exception as e:
#         return HttpResponse(None)
#     number = city.number
#     url1 = 'http://www.weather.com.cn/weather/'
#     url2 = '.shtml'
#     url = url1 + number + url2
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
#     }
#     html = requests.get(url, headers=headers)
#     html.encoding = 'utf-8'
#     htmlText = html.text
#     soup = BeautifulSoup(html.text, 'html.parser')
#     lis = soup.find_all('li', class_='sky')
#     tianqi = []
#     for li in lis:
#         dic = {}
#         h1_dates = li.find_all('h1')[0].get_text()
#         p_weas = li.find_all('p', class_='wea')[0].get_text()
#         p_tems = li.find_all('p', class_='tem')[0].get_text()
#         p_wins = li.find_all('p', class_='win')[0].get_text()
#         dic['date'] = h1_dates
#         dic['weather'] = p_weas
#         dic['templerature'] = p_tems
#         dic['win'] = p_wins
#         tianqi.append(dic)
#     print(tianqi)
#     return tianqi

# 获取所有景点信息
# def get_data(request,address):
#     shi=address.split('&')[0]
#     qu=address.split('&')[1]
#     print('俺获取到景点的城市啦')
#     view_qu = CityInfo.objects.filter(city_obj=qu)
#     print(view_qu)
#     if not view_qu:
#         view_shi = CityInfo.objects.filter(city_obj=shi)
#         if not view_shi:
#             result = {'code': 1000, 'error': 'no any views in here'}
#             return JsonResponse(result)
#         view_qu=view_shi
#     view_list=[]
#     print('44444444444',view_qu)
#     for view in view_qu:
#         # print(view.city_obj)
#         view_dict = {}
#         view_dict['city_name'] = view.city_obj
#         view_dict['view_name'] = view.view_name
#         view_dict['view_id'] = view.id
#         view_dict['view_address'] = view.view_address
#         view_dict['view_score'] = view.view_score
#         view_dict['view_price'] = view.view_price
#         view_dict['view_img'] = view.view_img
#         tq=get_weather(view.city_obj)
#         view_dict['view_tq'] = tq[0]
#         view_list.append(view_dict)
#     print(view_list)
#     # result={'code':200,'data':view_list}
#     result = {'code': 200, 'data': view_list}
#
#     # print('333333333',result)
#     return JsonResponse(result)


# 获取所有景点信息

# 获取景点信息

def get_data(request, address):
    shi = address.split('&')[0]
    print('shi', shi)
    qu = address.split('&')[1]
    print('qu', qu)
    print('俺获取到景点的城市啦')
    view_qu_list = cache_dec(qu, 0)
    if not view_qu_list:
        view_shi_list = cache_dec(shi, 0)
        if not view_shi_list:
            result = {'code': 1000, 'error': 'no any views in here'}
            return JsonResponse(result)
        result = {'code': 200, 'data': view_shi_list}
        return JsonResponse(result)
    result = {'code': 200, 'data': view_qu_list}
    return JsonResponse(result)


# get请求返回景点推荐的页面
def get_viewlist(request):
    if request.method == 'GET':
        return render(request, 'customized/view.html')


# 返回当前地址
def return_address(request, address):
    address_dict = get_addree(address)
    # print(address_dict)
    if not address_dict['shi'] or not address_dict['qu']:
        result = {'code': '1001', "error": 'don not match any city'}
        return JsonResponse(result)
    if not address_dict['qu']:
        result = {'code': '200', 'address': address_dict['shi'], 'data': address_dict}
        return JsonResponse(result)
    result = {'code': '200', 'address': address_dict['qu'], "data": address_dict}
    # print(result)
    return JsonResponse(result)


def get_view(request, address):
    return render(request, 'customized/search_view.html')
