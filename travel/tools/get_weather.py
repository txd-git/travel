import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from tq.models import City

def get_weather(position):
    # print('9999999999999',position)
    try:
        city = City.objects.get(city_name=position)
        # print('000000000000',city.number)
    except Exception as e:
        return None
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
    try:
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
        print(position,'shsuichdcnjhwdhwdnwelxwlx', tianqi)
        return tianqi
    except Exception as e:
        return None



