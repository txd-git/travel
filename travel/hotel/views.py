from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from alipay import AliPay
from django.conf import settings

import json


# Create your views here.
def get_info(request):
    if request.method == 'GET':
        return render(request, 'hotel/hotel.html')

# 装饰器
from django.utils.decorators import method_decorator
from tools.logging_dec import logging_check

# Create your views here.
app_private_key_string = open(settings.ALIPAY_KEY_DIR + 'app_private_key.pem').read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIR + 'alipay_public_key.pem').read()

ORDER_STATUAS = 1  # 1 待付款  2 已付款 3 付款失败


# 定义一个alipay视图类(基类),负责初始化支付相关的参数的
class MyAlipay(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True
        )
        print(settings.ALIPAY_APP_ID)

    def get_trade_url(self, order_id, amount):
        base_url = 'https://openapi.alipaydev.com/gateway.do'
        order_string = self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=amount,
            subject=order_id,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL
        )
        return base_url + '?' + order_string

    def get_trade_result(self, order_id):
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get('trade_status') == 'TRADE_SUCCESS':
            return True
        return False

    def get_verify_result(self, data, sign):
        # 验证签名
        return self.alipay.verify(data, sign)


class BaoView(MyAlipay):
    def get(self, request):
        return render(request, 'hotel/hotel.html')

    @method_decorator(logging_check)
    def post(self, request):
        json_obj = json.loads(request.body)
        order_id = json_obj['order_id']
        price = json_obj['price']
        pay_url = self.get_trade_url(order_id, price)
        return JsonResponse({'code':200,'pay_url': pay_url})


class ResultView(MyAlipay):
    def get(self, request):
        # return_url ,不带支付信息，一般会从数据中查询订单信息
        request_data = {k: request.GET[k] for k in request.GET.keys()}
        # print('-----------------request data-----------------')
        # print(request_data)
        order_id = request_data['out_trade_no']
        if ORDER_STATUAS == 1:
            # 证明可能post有bug，需要我们【主动向支付宝的服务器查询】
            result = self.get_trade_result(order_id)
            if result:
                return HttpResponse('主动查询支付成功')
            else:
                return HttpResponse('支付失败')

    def post(self, request):
        # 支付完成后，post对应的url是ALIPAY_NOTIFY_URL[带支付信息的]
        # 讲支付宝服务器传递过来的数据转换为标准的Python字典
        request_data = {k: request.POST[k] for k in request.POST.keys()}
        # 取出数据中签名
        sign = request_data.pop('sign')
        # 验证数据是否由支付宝服务器发送
        is_verify = self.get_verify_result(request_data, sign)
        if is_verify:
            # 取出交易状态
            trade_status = request_data['trade_status']
            if trade_status == 'TRADE_SUCCESS':
                # 将数据库的订单状态修改为已付款
                return HttpResponse('ok')
            else:
                # 将数据库的订单状态修改为支付失败
                return HttpResponse('error')
        else:
            return HttpResponse('非法访问')
