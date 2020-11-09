import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from alipay import AliPay
from django.conf import settings
from user.models import UserProfile
from tools.logging_dec import logging_check
from tools.logging_dec import get_user_by_request
from django.utils.decorators import method_decorator
from .models import TicketPay
from user.models import UserProfile
from customized.models import CityInfo
# Create your views here.
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app_private_key_string=open(settings.ALIPAY_KEY_DIR+'app_private_key.pem').read()
alipay_public_key_string=open(settings.ALIPAY_KEY_DIR+'alipay_public_key.pem').read()


class MyAlipay(View):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.alipay=AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True
        )
        print('111111')

    def get_trade_url(self,order_id,amount):
        base_url='https://openapi.alipaydev.com/gateway.do'
        order_string=self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=amount,
            subject=order_id,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL
        )
        return base_url+'?'+order_string

    #从alipay查询结果
    def get_trade_result(self, order_id):
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        print('333333333',result)
        if result.get('trade_status') == 'TRADE_SUCCESS':
            return True
        return False



class JumpView(MyAlipay):
    @method_decorator(logging_check)
    def post(self,request):
        json_obj=json.loads(request.body)
        # print('223323323',json_obj)
        order_id=''.join(json_obj['order_id'].split('-'))
        print('eeeeeeeeeeeeeee',order_id)
        price=int(json_obj['price'])
        pay_url=self.get_trade_url(order_id,price)
        return JsonResponse({'pay_url':pay_url})



ORDER_STATUAS = 1
class ResultView(MyAlipay):

    def get(self,request):
        request_data = {k: request.GET[k] for k in request.GET.keys()}
        print('get_data',request_data)
        order_id=request_data['out_trade_no']
        print('rrrrrrrrrrrrrrrrrrr',order_id)
        spend_time = order_id[:8]
        print('spend_time',spend_time)
        price=request_data['total_amount']
        if ORDER_STATUAS == 1:
            # 证明可能post有bug，需要我们【主动向支付宝的服务器查询】
            result = self.get_trade_result(order_id)
            print(result)
            if result:
                return render(request,'customized/payok.html',locals())
            else:
                return HttpResponse('支付失败')
        # 切换页面，从数据库里查询订单信息
        # try:
        #     ss=TicketPay.objects.get(order_id=order_id)
        # except Exception as e:
        #     result=self.get_tarde_result(order_id)
        #     if result:
        #         return render(request, '/customized/pay_order.html', locals())
        #     return HttpResponse('支付失败')
        #
        # if ss.order_status=='TRADE_SUCCESS':
        #     return render(request,'/customized/pay_order.html',locals())
        #     # return HttpResponse('请携带您的身份按时到景点，祝您有一个愉快的时光')
        # return HttpResponse('支付失败')


    def get_verify_result(self,data,sign):
        #验证签名
        return self.alipay.verify(data,sign)


    def post(self,request):
        #支付完成后,post
        print('支付完成后的post')
        request_data={k:request.POST[k] for k in request.POST.keys()}
        print('post_data',request_data)
        sign=request_data.pop('sign')
        order_id = request_data['out_trade_no']
        spend_time=order_id[:8]
        is_verify=self.get_verify_result(request_data,sign)
        if is_verify:
            trade_status=request_data['trade_status']
            if trade_status=='TRADE_SUCCESS':
                user_name=get_user_by_request(request)
                try:
                    user=UserProfile.objects.get(username=user_name)
                except Exception as e:
                    # print(e)
                    return HttpResponse('非法访问')
                TicketPay.objects.create(order_id=order_id,order_status=request_data['trade_status'],trade_no=request_data['trade_no'],spend_buytime=spend_time,user=user)
                return HttpResponse('ok')
            else:
                return HttpResponse('error')
        else:
            return HttpResponse('非法访问')



# eqcqyc4148@sandbox.com


# def get_order_info(request):
#     user_name=get_user_by_request(request)
#     print('wwwwwwwwww',user_name)
#     user=UserProfile.objects.get(username=user_name)
#     print(user)
#     order_info=TicketPay.objects.filter(user=user)
#     order_list=[]
#     for order in order_info:
#         order_dict={}
#         view_id=order.order_id[9:]
#         view=CityInfo.objects.get(id=view_id)
#         order_dict['order_id']=order.order_id
#         order_dict['view_name']=view.view_name
#         order_dict['trade_no']=order.trade_no
#         order_dict['order_status']=order.order_status
#         order_dict['order_buytime']=order.order_buytime
#         order_dict['spend_buytime']=order.spend_buytime
#         order_dict['is_consumed']=order.is_consumed
#         order_dict['view_name']=order.is_consumed
#         order_list.append(order_dict)
#     return JsonResponse(order_list,safe=False)



# def get_order_page(request):
#     return render(request,'customized/pay_order.html')

#eqcqyc4148@sandbox.com