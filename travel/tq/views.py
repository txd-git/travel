import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import City


# Create your views here.
def get_location(request):
    if request.method == 'GET':
        return render(request, 'location/get_location.html')
    elif request.method == "POST":
        address = request.POST.get('address')
        print('地址为%s' % address)
        return HttpResponse(address)


def get_weather(request, position):
    print(position)
    try:
        city = City.objects.get(city_name=position)
        print(city.number)
    except Exception as e:
        return JsonResponse(None, safe=False)
    number = city.number
    url1 = 'http://www.weather.com.cn/weather/'
    url2 = '.shtml'
    url = url1 + number + url2
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
    }
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    htmlText = html.text
    soup = BeautifulSoup(html.text, 'html.parser')
    lis = soup.find_all('li', class_='sky')
    tianqi = []
    for li in lis:
        dic = {}
        h1_dates = li.find_all('h1')[0].get_text()
        p_weas = li.find_all('p', class_='wea')[0].get_text()
        p_tems = li.find_all('p', class_='tem')[0].get_text()
        p_wins = li.find_all('p', class_='win')[0].get_text()
        dic['date'] = h1_dates
        dic['weather'] = p_weas
        dic['templerature'] = p_tems
        dic['win'] = p_wins
        tianqi.append(dic)
    return JsonResponse(tianqi, safe=False)


def get_addree(request, position):
    shi = ''
    qu = ''
    address = position.split('省')[-1]
    for s in range(len(address)):
        if address[s] == '市':
            shi = address[:s]
            print(shi)
        for q in range(s, len(address)):
            if address[q] == '区' or address[q] == '县':
                qu = address[s + 1:q]

    # print(sheng, '|', shi, '|', qu)
    try:
        city = City.objects.get(city_name=qu)
        city_name = qu
    except Exception as e:
        city_name = shi
    return HttpResponse(city_name)


def get_name(request):
    city = City.objects.all()
    name = []
    dicname = {}
    for item in city:
        name.append(item.city_name)
    dicname["name"] = name

    return JsonResponse(dicname)
