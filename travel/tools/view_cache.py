from django.core.cache import cache
from django.http import JsonResponse
from tools.get_weather import get_weather
from customized.models import CityInfo
from tools.get_address import get_addree


#获取景点信息缓存设置
def cache_dec(address,expire):
    print('11111111111111111',address,'222222222222222')
    cache_content=cache.get('view:%s'%address)
    print('cache_content',cache_content)
    if cache_content:
        return cache_content
    else:
        print('ggggggggg',address)
        view = CityInfo.objects.filter(city_obj=address)
        print('sssssssssssss',view)
        if not view:
            return None
        view_list = []
        for view in view:
            # print(view.city_obj)
            print('view.view_address', view.view_address)
            view_dict = {}
            view_dict['city_name'] = view.city_obj
            view_dict['view_name'] = view.view_name
            view_dict['view_id'] = view.id
            view_dict['view_address'] = view.view_address
            view_dict['view_score'] = view.view_score
            view_dict['view_price'] = view.view_price
            view_dict['view_img'] = view.view_img
            view_address = get_addree(view.view_address)
            print('view_address',view_address)
            shiqu_list=[view_address['zhen'],view_address['qu'],view_address['shi']]
            print('shiqu_list',shiqu_list)
            zhen=view_address['zhen']
            qu=view_address['qu']
            shi=view_address['shi']
            zhen_weather=get_weather(zhen)
            print('zhen_weather',zhen_weather)
            qu_weather=get_weather(qu)
            print('qu_weather', qu_weather)
            shi_weather=get_weather(shi)

            print('shi_weather', shi_weather)
            if zhen_weather:
                view_dict['view_tq'] = zhen_weather[0]
            else:
                if qu_weather:
                    view_dict['view_tq'] = qu_weather[0]
                else:
                    if shi_weather:
                        view_dict['view_tq'] = shi_weather[0]
                    else:
                        dic = {}
                        dic['date'] = ''
                        dic['weather'] = ''
                        dic['templerature'] = ''
                        dic['win'] = ''
                        view_dict['view_tq'] = dic


            view_list.append(view_dict)
        print('返回的view_list',view_list)

        cache.set('view:%s'%address,view_list,expire)
        return view_list
















