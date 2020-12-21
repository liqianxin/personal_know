import pymongo
from pymongo.collection import Collection

import time
import datetime
import redis



r = redis.Redis(host='localhost', port=6379, db=0)

mongoclient = pymongo.MongoClient(host="112.126.93.104", port=12832)
db = mongoclient["user"]
user_table = db.user  # type: Collection
contract_table = db.contract  # type: Collection
user_recode = db.recode  # type: Collection

page_size = 10
user_info_num = user_table.find({}).count()
print(user_info_num)


# def now_btc_price(access_key, secret_key):
#     now_btc_obj = huobi_sdk.api_key_get('https://api.huobi.pro', '/market/detail/merged', {"symbol": "btcusdt"},
#                                         ACCESS_KEY=access_key, SECRET_KEY=secret_key)
#     btc_price = now_btc_obj['tick']['close']
#     return btc_price
'''
Email
'''
error_msg = """
<table style="width: 538px; background-color: #393836;" align="center" cellspacing="0" cellpadding="0">
    <tbody>

    <tr>
        <td bgcolor="#17212e">
            <table width="470" border="0" align="center" cellpadding="0" cellspacing="0"
                   style="padding-left: 5px; padding-right: 5px; padding-bottom: 10px;">
                <tbody>
                <tr bgcolor="#17212e">
                    <td style="padding-top: 32px;">
                        <span
                                style="padding-top: 16px; padding-bottom: 16px; font-size: 24px; color: #66c0f4; font-family: Arial, Helvetica, sans-serif; font-weight: bold;">您好！
                        </span>
				<br>
					</td>
                </tr>
                <tr>
                    <td style="padding-top: 12px;"><span
                            style="font-size: 17px; color: #c6d4df; font-family: Arial, Helvetica, sans-serif; font-weight: bold;"><p>核算脚本出错,请尽快修改！s%</p></span>
                    </td>
                </tr>

                <tr>
                    <td style="font-size: 12px; color: #6d7880; padding-top: 16px; padding-bottom: 60px;">深蓝AI量化 团队<br><a
                            style="color: #8f98a0;" href="https://baidu.com" rel="noopener" target="_blank">https://baidu.com</a><br>
                    </td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr>

    </tbody>
</table>
"""

msg = """
<table style="width: 538px; background-color: #393836;" align="center" cellspacing="0" cellpadding="0">
    <tbody>

    <tr>
        <td bgcolor="#17212e">
            <table width="470" border="0" align="center" cellpadding="0" cellspacing="0"
                   style="padding-left: 5px; padding-right: 5px; padding-bottom: 10px;">
                <tbody>
                <tr bgcolor="#17212e">
                    <td style="padding-top: 32px;">
                        <span
                                style="padding-top: 16px; padding-bottom: 16px; font-size: 24px; color: #66c0f4; font-family: Arial, Helvetica, sans-serif; font-weight: bold;">您好！
                        </span>
				<br>
					</td>
                </tr>
                <tr>
                    <td style="padding-top: 12px;"><span
                            style="font-size: 17px; color: #c6d4df; font-family: Arial, Helvetica, sans-serif; font-weight: bold;"><p>您所需的 深蓝AI量化 令牌验证码为：</p></span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div><span
                                style="font-size: 24px; color: #66c0f4; font-family: Arial, Helvetica, sans-serif; font-weight: bold;">{code}</span>
                        </div>
                    </td>
                </tr>
                <tr bgcolor="#121a25">
                    <td style="padding: 20px; font-size: 12px; line-height: 17px; color: #c6d4df; font-family: Arial, Helvetica, sans-serif;">
                        <p style="padding-bottom: 10px; color: #c6d4df;">深蓝AI量化 令牌验证码是完成登录所必需的, 请于{time}分钟内输入。<span
                                style="color: #ffffff; font-weight: bold;">没有人能够不访问这封电子邮件就访问您的帐户。</span></p>
                        <p style="padding-bottom: 10px; color: #c6d4df;"><span
                                style="color: #ffffff; font-weight: bold;">如果不是你本人操作</span>，请直接忽略，或考虑更改您的电子邮件密码，以确保您的帐户安全。
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="font-size: 12px; color: #6d7880; padding-top: 16px; padding-bottom: 60px;">深蓝AI量化 团队<br><a
                            style="color: #8f98a0;" href="https://baidu.com" rel="noopener" target="_blank">https://baidu.com</a><br>
                    </td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr>

    </tbody>
</table>
"""

prompt_msg = """
<table style="width: 538px; background-color: #393836;" align="center" cellspacing="0" cellpadding="0">
    <tbody>

    <tr>
        <td bgcolor="#17212e">
            <table width="470" border="0" align="center" cellpadding="0" cellspacing="0"
                   style="padding-left: 5px; padding-right: 5px; padding-bottom: 10px;">
                <tbody>
                <tr bgcolor="#17212e">
                    <td style="padding-top: 32px;">
                        <span
                                style="padding-top: 16px; padding-bottom: 16px; font-size: 24px; color: #66c0f4; font-family: Arial, Helvetica, sans-serif; font-weight: bold;">您好！
                        </span>
				<br>
					</td>
                </tr>
                <tr>
                    <td style="padding-top: 12px;"><span
                            style="font-size: 17px; color: #c6d4df; font-family: Arial, Helvetica, sans-serif; font-weight: bold;"><p>您的保证金余额不足，请及时充值！</p></span>
                    </td>
                </tr>

                <tr>
                    <td style="font-size: 12px; color: #6d7880; padding-top: 16px; padding-bottom: 60px;">深蓝AI量化 团队<br><a
                            style="color: #8f98a0;" href="https://baidu.com" rel="noopener" target="_blank">https://baidu.com</a><br>
                    </td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr>

    </tbody>
</table>
"""


mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "943398251@qq.com"  # 用户名
mail_pass = "smocqbrxvswrbdge"  # 口令

sender = '943398251@qq.com'
# receivers = ['qizhg@ncist.edu.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

email_msg = msg
prompt_msg = prompt_msg
error_msg = error_msg
EMAIL_CODE_EXP = 2


import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_prompt_msg(email):
    receivers = email
    message = MIMEText(prompt_msg, 'html', 'utf-8')
    message['From'] = Header("DeepBlue", 'utf-8')
    message['To'] = Header("me", 'utf-8')

    subject = '【DeepBlue邮件】'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # 465 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except smtplib.SMTPException as e:
        ...


def send_error_msg(email, error_info):
    receivers = email
    message = MIMEText(error_msg.format(error_info), 'html', 'utf-8')
    message['From'] = Header("DeepBlue", 'utf-8')
    message['To'] = Header("me", 'utf-8')

    subject = '【DeepBlue邮件】'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # 465 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True
    except smtplib.SMTPException as e:
        ...






'''
HuobiDMUtil
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20180917
# @Author  : zhaobo
# @github  :

import base64
import hmac
import hashlib
import json

import urllib
import datetime
import requests
#import urlparse   # urllib.parse in python 3

# timeout in 5 seconds:
TIMEOUT = 5

#各种请求,获取数据方式
def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    try:
        response = requests.get(url, postdata, headers=headers, timeout=TIMEOUT, proxies={'https': 'http://127.0.0.1:1082'})
        if response.status_code == 200:
            return response.json()
        else:
            return {"status":"fail"}
    except Exception as e:
        print("httpGet failed, detail is:%s" %e)
        return {"status":"fail","msg": "%s"%e}

def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    try:
        response = requests.post(url, postdata, headers=headers, timeout=TIMEOUT, proxies={'https': 'http://127.0.0.1:1082'})
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status":"fail","msg": "%s"%e}


def api_key_get(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_name = host_url = url
    #host_name = urlparse.urlparse(host_url).hostname
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()

    params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = url
    #host_name = urlparse.urlparse(host_url).hostname
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature


# print(json.dumps(api_key_get('https://api.huobi.pro', '/market/detail/merged', {"symbol": "btcusdt"}, ACCESS_KEY='fb591f3c-b0e09be1-c4f9aaf2-bn2wed5t4y', SECRET_KEY='3efd4b91-51d8a5f0-4f6f5464-236ff')))
# print(json.dumps(api_key_post('https://api.hbdm.com', '/api/v1/contract_available_level_rate', {}, ACCESS_KEY='fb591f3c-b0e09be1-c4f9aaf2-bn2wed5t4y', SECRET_KEY='3efd4b91-51d8a5f0-4f6f5464-236ff')))






'''
HuobiDMService
'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 20180917
# @Author  : zhaobo
# @github  :




class HuobiDM:

    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key

    '''
    ======================
    Market data API
    ======================
    '''

    # 获取合约信息
    def get_contract_info(self, symbol='', contract_type='', contract_code=''):
        """
        参数名称         参数类型  必填    描述
        symbol          string  false   "BTC","ETH"...
        contract_type   string  false   合约类型: this_week:当周 next_week:下周 quarter:季度
        contract_code   string  false   BTC181228
        备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code

        url = self.__url + '/api/v1/contract_contract_info'
        return http_get_request(url, params)

    # 获取合约指数信息
    def get_contract_index(self, symbol):
        """
        :symbol    "BTC","ETH"...
        """
        params = {'symbol': symbol}

        url = self.__url + '/api/v1/contract_index'
        return http_get_request(url, params)

    # 获取合约最高限价和最低限价
    def get_contract_price_limit(self, symbol='', contract_type='', contract_code=''):
        """
        :symbol          "BTC","ETH"...
        :contract_type   合约类型: this_week:当周 next_week:下周 quarter:季度
        "contract_code   BTC180928
        备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code

        url = self.__url + '/api/v1/contract_price_limit'
        return http_get_request(url, params)

    # 获取当前可用合约总持仓量
    def get_contract_open_interest(self, symbol='', contract_type='', contract_code=''):
        """
        :symbol          "BTC","ETH"...
        :contract_type   合约类型: this_week:当周 next_week:下周 quarter:季度
        "contract_code   BTC180928
        备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
        """
        params = {'symbol': symbol,
                  'contract_type': contract_type,
                  'contract_code': contract_code}

        url = self.__url + '/api/v1/contract_open_interest'
        return http_get_request(url, params)

        # 获取行情深度

    def get_contract_depth(self, symbol, type):
        """
        :param symbol:   BTC_CW, BTC_NW, BTC_CQ , ...
        :param type: 可选值：{ step0, step1, step2, step3, step4, step5 （合并深度0-5）；step0时，不合并深度 }
        :return:
        """
        params = {'symbol': symbol,
                  'type': type}

        url = self.__url + '/market/depth'
        return http_get_request(url, params)

    # 获取KLine
    def get_contract_kline(self, symbol, period, size=150):
        """
        :param symbol  BTC_CW, BTC_NW, BTC_CQ , ...
        :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1week, 1mon }
        :param size: [1,2000]
        :return:
        """
        params = {'symbol': symbol,
                  'period': period}
        if size:
            params['size'] = size

        url = self.__url + '/market/history/kline'
        return http_get_request(url, params)

    # 获取聚合行情
    def get_contract_market_merged(self, symbol):
        """
        :symbol	    "BTC_CW","BTC_NW", "BTC_CQ" ...
        """
        params = {'symbol': symbol}

        url = self.__url + '/market/detail/merged'
        return http_get_request(url, params)

    # 获取市场最近成交记录
    def get_contract_trade(self, symbol, size=1):
        """
        :param symbol: 可选值：{ BTC_CW, BTC_NW, BTC_CQ, etc. }
        :return:
        """
        params = {'symbol': symbol,
                  'size': size}

        url = self.__url + '/market/trade'
        return http_get_request(url, params)

    # 批量获取最近的交易记录
    def get_contract_batch_trade(self, symbol, size=1):
        """
        :param symbol: 可选值：{ BTC_CW, BTC_NW, BTC_CQ, etc. }, size: int
        :return:
        """
        params = {'symbol': symbol,
                  'size': size}

        url = self.__url + '/market/history/trade'
        return http_get_request(url, params)

    '''
    ======================
    Trade/Account API
    ======================
    '''

    # 获取用户账户信息
    def get_contract_account_info(self, symbol=''):
        """
        :param symbol: "BTC","ETH"...如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params["symbol"] = symbol

        request_path = '/api/v1/contract_account_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户持仓信息
    def get_contract_position_info(self, symbol=''):
        """
        :param symbol: "BTC","ETH"...如果缺省，默认返回所有品种
        :return:
        """

        params = {}
        if symbol:
            params["symbol"] = symbol

        request_path = '/api/v1/contract_position_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 合约下单
    def send_contract_order(self, symbol, contract_type, contract_code,
                            client_order_id, price, volume, direction, offset,
                            lever_rate, order_price_type):
        """
        :symbol: "BTC","ETH"..
        :contract_type: "this_week", "next_week", "quarter"
        :contract_code: "BTC181228"
        :client_order_id: 客户自己填写和维护，这次一定要大于上一次
        :price             必填   价格
        :volume            必填  委托数量（张）
        :direction         必填  "buy" "sell"
        :offset            必填   "open", "close"
        :lever_rate        必填  杠杆倍数
        :order_price_type  必填   "limit"限价， "opponent" 对手价
        备注：如果contract_code填了值，那就按照contract_code去下单，如果contract_code没有填值，则按照symbol+contract_type去下单。
        :
        """

        params = {"price": price,
                  "volume": volume,
                  "direction": direction,
                  "offset": offset,
                  "lever_rate": lever_rate,
                  "order_price_type": order_price_type}
        if symbol:
            params["symbol"] = symbol
        if contract_type:
            params['contract_type'] = contract_type
        if contract_code:
            params['contract_code'] = contract_code
        if client_order_id:
            params['client_order_id'] = client_order_id

        request_path = '/api/v1/contract_order'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 合约批量下单
    def send_contract_batchorder(self, orders_data):
        """
        orders_data: example:
        orders_data = {'orders_data': [
               {'symbol': 'BTC', 'contract_type': 'quarter',
                'contract_code':'BTC181228',  'client_order_id':'',
                'price':1, 'volume':1, 'direction':'buy', 'offset':'open',
                'leverRate':20, 'orderPriceType':'limit'},
               {'symbol': 'BTC','contract_type': 'quarter',
                'contract_code':'BTC181228', 'client_order_id':'',
                'price':2, 'volume':2, 'direction':'buy', 'offset':'open',
                'leverRate':20, 'orderPriceType':'limit'}]}

        Parameters of each order: refer to send_contract_order
        """

        params = orders_data
        request_path = '/api/v1/contract_batchorder'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 撤销订单
    def cancel_contract_order(self, symbol, order_id='', client_order_id=''):
        """
        参数名称          是否必须 类型     描述
        symbol           true   string  BTC, ETH, ...
        order_id	         false  string  订单ID（ 多个订单ID中间以","分隔,一次最多允许撤消50个订单 ）
        client_order_id  false  string  客户订单ID(多个订单ID中间以","分隔,一次最多允许撤消50个订单)
        备注： order_id 和 client_order_id都可以用来撤单，同时只可以设置其中一种，如果设置了两种，默认以order_id来撤单。
        """

        params = {"symbol": symbol}
        if order_id:
            params["order_id"] = order_id
        if client_order_id:
            params["client_order_id"] = client_order_id

        request_path = '/api/v1/contract_cancel'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 全部撤单
    def cancel_all_contract_order(self, symbol):
        """
        symbol: BTC, ETH, ...
        """

        params = {"symbol": symbol}

        request_path = '/api/v1/contract_cancelall'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约订单信息
    def get_contract_order_info(self, symbol, order_id='', client_order_id=''):
        """
        参数名称	        是否必须	类型	    描述
        symbol          true    string  BTC, ETH, ...
        order_id	        false	string	订单ID（ 多个订单ID中间以","分隔,一次最多允许查询20个订单 ）
        client_order_id	false	string	客户订单ID(多个订单ID中间以","分隔,一次最多允许查询20个订单)
        备注：order_id和client_order_id都可以用来查询，同时只可以设置其中一种，如果设置了两种，默认以order_id来查询。
        """

        params = {"symbol": symbol}
        if order_id:
            params["order_id"] = order_id
        if client_order_id:
            params["client_order_id"] = client_order_id

        request_path = '/api/v1/contract_order_info'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约订单明细信息

    def get_contract_order_detail(self, symbol, order_id, order_type, created_at, page_index=None, page_size=None):
        """
        参数名称     是否必须  类型    描述
        symbol      true	    string "BTC","ETH"...
        order_id    true	    long	   订单id
        order_type  true    int    订单类型。1:报单， 2:撤单， 3:爆仓， 4:交割
        created_at  true    number 订单创建时间
        page_index  false   int    第几页,不填第一页
        page_size   false   int    不填默认20，不得多于50
        """

        params = {"symbol": symbol,
                  "order_id": order_id,
                  "order_type": order_type,
                  "created_at": created_at}
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size

        request_path = '/api/v1/contract_order_detail'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约当前未成交委托
    def get_contract_open_orders(self, symbol=None, page_index=None, page_size=None):
        """
        参数名称     是否必须  类型   描述
        symbol      false   string "BTC","ETH"...
        page_index  false   int    第几页,不填第一页
        page_size   false   int    不填默认20，不得多于50
        """

        params = {}
        if symbol:
            params["symbol"] = symbol
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size

        request_path = '/api/v1/contract_openorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取合约历史委托
    def get_contract_history_orders(self, symbol, trade_type, type, status, create_date,
                                    page_index=None, page_size=None):
        """
        参数名称     是否必须  类型     描述	    取值范围
        symbol      true	    string  品种代码  "BTC","ETH"...
        trade_type  true	    int     交易类型  0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多,5: 卖出强平,6: 买入强平,7:交割平多,8: 交割平空
        type        true	    int     类型     1:所有订单、2：结束汏订单
        status      true	    int     订单状态  0:全部,3:未成交, 4: 部分成交,5: 部分成交已撤单,6: 全部成交,7:已撤单
        create_date true	    int     日期     7，90（7天或者90天）
        page_index  false   int     页码，不填默认第1页
        page_size   false   int     不填默认20，不得多于50
        """

        params = {"symbol": symbol,
                  "trade_type": trade_type,
                  "type": type,
                  "status": status,
                  "create_date": create_date}
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size

        request_path = '/api/v1/contract_hisorders'
        return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)





'''
huobi_sdk
'''
import base64
import hmac
import hashlib
import json

import urllib
import datetime
import requests
import time
# from . import logger

# TIMEOUT = 5
#
#
# #各种请求,获取数据方式
# def http_get_request(url, params, add_to_headers=None):
#     headers = {
#         "Content-type": "application/x-www-form-urlencoded",
#         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
#     }
#     if add_to_headers:
#         headers.update(add_to_headers)
#     postdata = urllib.parse.urlencode(params)
#     try:
#         response = requests.get(url, postdata, headers=headers, timeout=TIMEOUT, proxies={'https': 'http://127.0.0.1:1082'})
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"status":"fail"}
#     except Exception as e:
#         print("httpGet failed, detail is:%s" %e)
#         return {"status":"fail","msg": "%s"%e}
#
#
# def http_post_request(url, params, add_to_headers=None):
#     headers = {
#         "Accept": "application/json",
#         'Content-Type': 'application/json',
#         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
#     }
#     if add_to_headers:
#         headers.update(add_to_headers)
#     postdata = json.dumps(params)
#     try:
#         response = requests.post(url, postdata, headers=headers, timeout=TIMEOUT, proxies={'https': 'http://127.0.0.1:1082'})
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return response.json()
#     except Exception as e:
#         print("httpPost failed, detail is:%s" % e)
#         return {"status":"fail","msg": "%s"%e}
#
#
# def api_key_get(url, request_path, params, ACCESS_KEY, SECRET_KEY):
#     method = 'GET'
#     timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
#     params.update({'AccessKeyId': ACCESS_KEY,
#                    'SignatureMethod': 'HmacSHA256',
#                    'SignatureVersion': '2',
#                    'Timestamp': timestamp})
#
#     host_name = host_url = url
#     #host_name = urlparse.urlparse(host_url).hostname
#     host_name = urllib.parse.urlparse(host_url).hostname
#     host_name = host_name.lower()
#
#     params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)
#     url = host_url + request_path
#     return http_get_request(url, params)
#
#
# def api_key_post(url, request_path, params, ACCESS_KEY, SECRET_KEY):
#     method = 'POST'
#     timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
#     params_to_sign = {'AccessKeyId': ACCESS_KEY,
#                       'SignatureMethod': 'HmacSHA256',
#                       'SignatureVersion': '2',
#                       'Timestamp': timestamp}
#
#     host_url = url
#     #host_name = urlparse.urlparse(host_url).hostname
#     host_name = urllib.parse.urlparse(host_url).hostname
#     host_name = host_name.lower()
#     params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
#     url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
#     return http_post_request(url, params)
#
#
# def createSign(pParams, method, host_url, request_path, secret_key):
#     sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
#     encode_params = urllib.parse.urlencode(sorted_params)
#     payload = [method, host_url, request_path, encode_params]
#     payload = '\n'.join(payload)
#     payload = payload.encode(encoding='UTF8')
#     secret_key = secret_key.encode(encoding='UTF8')
#     digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
#     signature = base64.b64encode(digest)
#     signature = signature.decode()
#     return signature


class HuobiAPI:


    def __init__(self, ACCESS_KEY, SECRET_KEY):
        self.ACCESS_KEY = ACCESS_KEY
        self.SECRET_KEY = SECRET_KEY
        self.dm = HuobiDM(huobidm_domain, ACCESS_KEY, SECRET_KEY)
        res = self.ensure_status_ok(api_key_get, (spot_domain, '/v1/account/accounts', {}, self.ACCESS_KEY, self.SECRET_KEY))
        spot_account = [el for el in res['data'] if el['type'] == 'spot']
        assert len(spot_account) == 1
        spot_account = spot_account[0]['id']
        self.spot_account_id = spot_account

    def get_gold_standard_0_position_zhang(self, return_all=False):
        res = self.ensure_status_ok(api_key_post, [huobidm_domain, '/api/v1/contract_account_info', {'symbol': 'BTC'}, self.ACCESS_KEY, self.SECRET_KEY])
        assert len(res['data']) == 1
        margin_balance = res['data'][0]['margin_balance']  # BTC 数量
        btc_price = self.get_quarter_price()
        margin_balance_usd = margin_balance * btc_price
        gold_standard_0_position_zhang = margin_balance_usd / ZHANG_UNIT
        assert gold_standard_0_position_zhang >= 0
        if not return_all:
            return gold_standard_0_position_zhang
        else:
            return gold_standard_0_position_zhang, margin_balance, btc_price

    def spot_cancel_all_order(self):
        # {'status': 'ok', 'data': {'success-count': 0, 'failed-count': 0, 'next-id': -1}}
        res = self.ensure_status_ok(api_key_post, [spot_domain, '/v1/order/orders/batchCancelOpenOrders', {}, self.ACCESS_KEY, self.SECRET_KEY])
        return res

    def spot_place_order(self, params):
        res = api_key_post(spot_domain, '/v1/order/orders/place', params, self.ACCESS_KEY, self.SECRET_KEY)
        return res

    def check_high_leverage_available(self, leverage=100):
        res = self.ensure_status_ok(api_key_post,
                                    [huobidm_domain, '/api/v1/contract_available_level_rate', {'symbol': "BTC"},
                                     self.ACCESS_KEY, self.SECRET_KEY])
        available_leverage = [el for el in res['data'] if el['symbol'] == 'BTC']
        assert len(available_leverage) == 1
        available_leverage = available_leverage[0]['available_level_rate']
        available_leverage = [int(el) for el in available_leverage.split(',')]
        # '1,2,3,5,10,20'
        # '1,2,3,5,10,20,30,50,75,100,125'
        if int(leverage) in available_leverage:
            return True
        else:
            return False

    def get_spot_btcusdt_price(self, return_bid_ask=False):
        """
        {'ch': 'market.btcusdt.depth.step0',
         'status': 'ok',
         'tick': {'asks': [[17000.03, 0.4716179451277439],
                           [17001.11, 0.003],
                           [17001.13, 0.0308],
                           [17003.56, 0.017],
                           [17004.54, 0.006]],
                  'bids': [[17000.02, 2.090637],
                           [17000.01, 1.552811],
                           [17000.0, 1.103142],
                           [16999.0, 0.01],
                           [16997.75, 0.1]],
                  'ts': 1606399446900,
                  'version': 115724410873},
         'ts': 1606399447748}
        """
        """
         {"status":"fail"}       
        """
        while 1:
            res = http_get_request(spot_domain + '/market/depth', {'symbol': 'btcusdt', 'depth': 5, 'type': 'step0'})
            if res['status'] == 'ok':
                price = {'bid': res['tick']['bids'][0][0], 'ask': res['tick']['asks'][0][0]}
                if return_bid_ask:
                    return price
                else:
                    return (price['ask'] + price['bid']) / 2

    def get_spot_usdt_withdraw_amount(self):
        """
           {'balance': '0', 'currency': 'ogn', 'type': 'frozen'},
           {'balance': '169.08085914',
            'currency': 'usdt',
            'type': 'trade'},
           {'balance': '0', 'currency': 'usdt', 'type': 'frozen'},
        """
        #
        # # 获得币币账户的号码
        # if self.spot_account_id is None:
        #     res = self.ensure_status_ok(api_key_get, (spot_domain, '/v1/account/accounts', {}, self.ACCESS_KEY, self.SECRET_KEY))
        #     spot_account = [el for el in res['data'] if el['type'] == 'spot']
        #     assert len(spot_account) == 1
        #     spot_account = spot_account[0]['id']
        #     self.spot_account_id = spot_account

        # 通过币币账户的号码获得币币账户的 BTC 数量
        res = self.ensure_status_ok(api_key_get, (spot_domain, f'/v1/account/accounts/{self.spot_account_id}/balance', {}, self.ACCESS_KEY, self.SECRET_KEY))
        res = [el for el in res['data']['list'] if el['currency'] == 'usdt' and el['type'] == 'trade']
        assert len(res) == 1
        spot_usdt = float(res[0]['balance'])
        return spot_usdt

    def check_sub_account(self):
        res = self._check_sub_account()
        if res['status'] == 'error' and res['err_code'] == 1018:
            return True
        else:
            return False


    def _check_sub_account(self):
        """{'status': 'error', 'err_code': 1018, 'err_msg': 'Main account doesnt exist.', 'ts': 1606025162666}"""
        """{'status': 'ok', 'data': [{'sub_uid': 136867614, 'list': [{'symbol': 'BSV', 'margin_balance': 0, 'liquidation_price': None, 'risk_rate': None}, {'symbol': 'BCH', 'margin_balance': 0,"""
        c = 1
        while 1:
            try:
                res = api_key_post(huobidm_domain, '/api/v1/contract_sub_account_list', {}, self.ACCESS_KEY , self.SECRET_KEY)
                if 'status' in res:
                    return res
            except:
                # if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                #     logging.warning(f'check_sub_account方法第{c - 1}次报错, {traceback.format_exc()}')
                #     my_email(f'lineno: {lineno()}, check_sub_account方法第{c - 1}次报错', traceback.format_exc())
                print(666)
            c += 1
            time.sleep(1)

    def get_order_residual(self, order_id):
        res = self.get_contract_order_info(order_id)
        volume = int(res['data'][0]['volume'])
        trade_volume = int(res['data'][0]['trade_volume'])
        residual = volume - trade_volume
        return residual, volume , trade_volume

    # @staticmethod
    def get_contract_order_info(self, order_id):
        """{'data': [{'canceled_at': 1606042963890,
           'client_order_id': None,
           'contract_code': 'BTC201225',
           'contract_type': 'quarter',
           'created_at': 1606042806591,
           'direction': 'sell',
           'fee': 0,
           'fee_asset': 'BTC',
           'lever_rate': 100,
           'liquidation_type': '0',
           'margin_frozen': 0.0,
           'offset': 'open',
           'order_id': 780145604818694145,
           'order_id_str': '780145604818694145',
           'order_price_type': 'limit',
           'order_source': 'api',
           'order_type': 1,
           'price': 20000,
           'profit': 0,
           'status': 7,
           'symbol': 'BTC',
           'trade_avg_price': None,
           'trade_turnover': 0,
           'trade_volume': 0,
           'volume': 1}],
        'status': 'ok',
        'ts': 1606042964911}"""

        c = 1
        while 1:
            try:
                res = self.dm.get_contract_order_info(symbol='BTC', order_id=order_id)
                if res['status'] == 'ok' and len(res['data']) == 1:
                    return res
            except:
                # if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                #     logging.warning(f'get_contract_order_info方法第{c - 1}次报错, {traceback.format_exc()}')
                #     my_email(f'lineno: {lineno()}, get_contract_order_info方法第{c - 1}次报错', traceback.format_exc())
                print(666)
            c += 1
            time.sleep(1)

    # @staticmethod
    def place_order(self, zhang, direction, offset, contract_type):
        """
        {'status': 'ok', 'data': {'order_id': 779776450755874816, 'order_id_str': '779776450755874816'}, 'ts': 1605954793408}

        全部以对手价下单
        开平方向
        开多：买入开多(direction用buy、offset用open)
        平多：卖出平多(direction用sell、offset用close)
        开空：卖出开空(direction用sell、offset用open)
        平空：买入平空(direction用buy、offset用close)
        """
        symbol = 'BTC'

        lever_rate = 100
        order_price_type = 'opponent'
        try:
            res = self.dm.send_contract_order(
                symbol,
                contract_type,
                contract_code=None,
                client_order_id=None,
                price=None,
                volume=zhang,
                direction=direction,
                offset=offset,
                lever_rate=lever_rate,
                order_price_type=order_price_type)
        except Exception as e:
            res = {'status': 'error', 'error': e}
        return res

    # @staticmethod
    def get_exchange_position(self, return_detail=False):
        """{'data': [{'available': 1.0,
           'contract_code': 'BTC201127',
           'contract_type': 'this_week',
           'cost_hold': 18513.300000000003,
           'cost_open': 18513.300000000003,
           'direction': 'sell',
           'frozen': 0.0,
           'last_price': 18517.33,
           'lever_rate': 100,
           'position_margin': 5.4003465942444e-05,
           'profit': -1.1755546971e-06,
           'profit_rate': -0.0217633967747915,
           'profit_unreal': -1.1755546971e-06,
           'symbol': 'BTC',
           'volume': 1.0},
          {'available': 1.0,
           'contract_code': 'BTC201204',
           'contract_type': 'next_week',
           'cost_hold': 18538.690000000002,
           'cost_open': 18538.690000000002,
           'direction': 'buy',
           'frozen': 0.0,
           'last_price': 18538.69,
           'lever_rate': 100,
           'position_margin': 5.3941243960603e-05,
           'profit': 0.0,
           'profit_rate': -5.6e-15,
           'profit_unreal': 0.0,
           'symbol': 'BTC',
           'volume': 1.0},
          {'available': 1.0,
           'contract_code': 'BTC201225',
           'contract_type': 'quarter',
           'cost_hold': 18638.36,
           'cost_open': 18638.36,
           'direction': 'buy',
           'frozen': 0.0,
           'last_price': 18640,
           'lever_rate': 100,
           'position_margin': 5.3648068669527e-05,
           'profit': 4.720524372e-07,
           'profit_rate': 0.0087982832617951,
           'profit_unreal': 4.720524372e-07,
           'symbol': 'BTC',
           'volume': 1.0},
          {'available': 0.0,
           'contract_code': 'BTC201225',
           'contract_type': 'quarter',
           'cost_hold': 18570.710000000003,
           'cost_open': 18570.710000000003,
           'direction': 'sell',
           'frozen': 1.0,
           'last_price': 18640,
           'lever_rate': 100,
           'position_margin': 5.3648068669527e-05,
           'profit': -2.00168689195e-05,
           'profit_rate': -0.3717274678111436,
           'profit_unreal': -2.00168689195e-05,
           'symbol': 'BTC',
           'volume': 1.0},
          {'available': 1.0,
           'contract_code': 'BTC210326',
           'contract_type': 'next_quarter',
           'cost_hold': 19200.0,
           'cost_open': 19200.0,
           'direction': 'buy',
           'frozen': 0.0,
           'last_price': 18955.69,
           'lever_rate': 100,
           'position_margin': 5.2754608246916e-05,
           'profit': -6.71274913583e-05,
           'profit_rate': -1.2888478340804328,
           'profit_unreal': -6.71274913583e-05,
           'symbol': 'BTC',
           'volume': 1.0}],
            'status': 'ok',
            'ts': 1606032830785}"""
        c = 1
        while 1:
            try:

                res = self.dm.get_contract_position_info("BTC")
                if res['status'] == 'ok':
                    long_zhang = 0
                    short_zhang = 0
                    # if len(res['data']) > 2:
                    #     logger.log.info(f'{res}')

                    detail = {
                        'this_week': {'buy': 0, 'sell': 0},
                        'next_week': {'buy': 0, 'sell': 0},
                        'quarter': {'buy': 0, 'sell': 0},
                        'next_quarter': {'buy': 0, 'sell': 0}
                    }
                    for dic in res['data']:
                        contract_type = dic['contract_type']
                        direction = dic['direction']
                        volume = dic['volume']
                        assert volume >= 0
                        assert detail[contract_type][direction] == 0
                        detail[contract_type][direction] += volume
                        if dic['direction'] == 'buy':
                            long_zhang += int(dic['volume'])
                        if dic['direction'] == 'sell':
                            short_zhang += int(dic['volume'])
                    if not return_detail:
                        return long_zhang, short_zhang
                    else:
                        return long_zhang, short_zhang, detail
            except:
                # if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                #     logging.warning(f'get_exchange_position方法第{c - 1}次报错, {traceback.format_exc()}')
                #     my_email(f'lineno: {lineno()}, get_exchange_position方法第{c - 1}次报错', traceback.format_exc())
                print(666)
            c += 1
            time.sleep(1)

    @staticmethod
    def ensure_status_ok(fun, params_list):
        def check_status_ok(res):
            if res['status'] == 'ok':
                return True
            else:
                return False

        while 1:
            try:
                res = fun(*params_list)
                if check_status_ok(res):
                    return res
            except:
                time.sleep(3)

    def get_btc_withdraw_amount(self):
        """获得币币账户可交易 + 合约账户可提币 BTC 数量"""
        if self.spot_account_id is None:
            # 获得币币账户的号码
            res = self.ensure_status_ok(api_key_get, (spot_domain, '/v1/account/accounts', {}, self.ACCESS_KEY, self.SECRET_KEY))
            spot_account = [el for el in res['data'] if el['type'] == 'spot']
            assert len(spot_account) == 1
            spot_account = spot_account[0]['id']
            self.spot_account_id = spot_account

        # 通过币币账户的号码获得币币账户的 BTC 数量
        res = self.ensure_status_ok(api_key_get, (spot_domain, f'/v1/account/accounts/{self.spot_account_id}/balance', {}, self.ACCESS_KEY, self.SECRET_KEY))
        res = [el for el in res['data']['list'] if el['currency'] == 'btc' and el['type'] == 'trade']
        assert len(res) == 1
        spot_btc = res[0]['balance']

        # 获得交割合约的 BTC 数量, 和有没有仓位
        futures_btc_info = self.dm.get_contract_account_info("BTC")['data'][0]
        futures_btc = futures_btc_info['withdraw_available']
        have_position = futures_btc_info['margin_position']
        have_position = True if have_position else False

        return float(spot_btc), float(futures_btc), have_position

    # @staticmethod
    def have_position(self):
        futures_btc_info = self.dm.get_contract_account_info("BTC")['data'][0]
        have_position = futures_btc_info['margin_position']
        have_position = True if have_position else False
        return have_position

    def transfer_btc(self, amount, to_spot, currency="btc"):
        channel = '/v1/futures/transfer'
        assert type(to_spot) == bool
        amount = str(amount).split('.')
        amount[1] = amount[1][:6]
        amount = amount[0] + '.' + amount[1]

        params = {
            "currency": currency,
            "amount": amount,
            "type": "futures-to-pro" if to_spot else "pro-to-futures",
        }
        print(params)
        res = api_key_post(spot_domain, channel, params, self.ACCESS_KEY, self.SECRET_KEY)
        return res

    # @staticmethod
    def cancel_all_order(self):
        """{'data': {'errors': [], 'successes': '779774592629473280,779774872988471296'},
         'status': 'ok',
         'ts': 1605954526488}"""
        c = 1
        while 1:
            try:
                res = self.dm.cancel_all_contract_order(symbol='BTC')
                if (res['err_msg'] == 'No orders to cancel.') or (res['status'] == 'ok' and res['data']['errors'] == []):
                    return res
            except:
                # if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                #     logger.log.warning(f'取消所有订单的方法第{c - 1}次报错, {traceback.format_exc()}')
                #     my_email(f'lineno: {lineno()}, 取消所有订单的方法第{c - 1}次报错', traceback.format_exc())
                print(666)
            c += 1
            time.sleep(1)

    # @staticmethod
    def get_quarter_price(self, return_dict=False):
        """{'ch': 'market.BTC_CQ.depth.step6',
         'status': 'ok',
         'tick': {'asks': [[18712.94, 3174],
                           [18712.95, 108],
                           [18714.13, 139]],
                  'bids': [[18712.93, 84],
                           [18712.01, 60],
                           [18712, 2]],
                  'ch': 'market.BTC_CQ.depth.step6',
                  'id': 1605958823,
                  'mrid': 115416923249,
                  'ts': 1605958823416,
                  'version': 1605958823},
         'ts': 1605958823439}"""
        c = 1
        while 1:
            try:
                res = self.dm.get_contract_depth(symbol='BTC_CQ', type='step6')
                if res['status'] == 'ok':
                    bid = res['tick']['bids'][0][0]
                    ask = res['tick']['asks'][0][0]
                    if not return_dict:
                        price = (bid + ask) / 2
                        return price
                    else:
                        return {'bid': bid, 'ask': ask}
            except:
                # if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                #     logger.log.warning(f'get_quarter_price方法第{c - 1}次报错, {traceback.format_exc()}')
                #     my_email(f'lineno: {lineno()}, get_quarter_price方法第{c - 1}次报错', traceback.format_exc())
                print(666)
            c += 1
            time.sleep(0.5)

spot_domain = 'https://api.huobi.pro'
huobidm_domain = 'https://api.hbdm.com'
































'''
核算脚本
'''
# 该协议的usdt数
def this_assets(exchange, cash_model, huobi_obj, btc_price):
    now_usdt = 0
    if exchange == "huobi":
        if cash_model == 'bitcoin':
            spot_btc_now, _, _ = huobi_obj.get_btc_withdraw_amount()
            now_usdt = spot_btc_now * btc_price
        else:
            spot_usdt_now = huobi_obj.get_spot_usdt_withdraw_amount()
            now_usdt = spot_usdt_now
    else:
        ...
    return now_usdt


def online_contract_assets(online_contract_list):
    sum = 0
    contract_obj = contract_table.find_one({"_id": online_contract_list[0]})
    api = contract_obj['api']
    access_key = api['access_key']
    secret_key = api['secret_key']
    huobi_api = HuobiAPI(ACCESS_KEY=access_key, SECRET_KEY=secret_key)
    btc_price = huobi_api.get_spot_btcusdt_price()
    for contract_obj_id in online_contract_list:
        contract_obj = contract_table.find_one({"_id": contract_obj_id})
        cash_model = contract_obj['本位']
        exchange = contract_obj['交易所']
        # 该协议资产总数
        usdt_num = this_assets(exchange, cash_model, huobi_api, btc_price)
        sum += usdt_num

    return sum


# 格式化时间转时间戳
def format_to_timestamp(format_time):
    now_format_time = format_time.strftime('%Y-%m-%d %H:%M:%S')
    struct_time = time.strptime(now_format_time, '%Y-%m-%d %X')
    timestamp = time.mktime(struct_time)
    return timestamp


# 不同类型用户（“散户”或“大户”）结算时的时间戳
def ord_settle_time(user_type, time_stamp):
    struct_time = time.localtime(time_stamp)
    format_time = time.strftime("%Y-%m-%d %X", struct_time)
    if user_type == "散户":
        format_end_time = datetime.datetime.strptime(format_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(15)
        end_time = format_to_timestamp(format_end_time)
    else:
        format_end_time = datetime.datetime.strptime(format_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(90)
        end_time = format_to_timestamp(format_end_time)
    return end_time


# 账户中货币数量（usdt或btc）
def account_assets(exchange, cash_mode, huobi_api):
    account_money = 0
    if exchange == "huobi":
        if cash_mode == 'bitcoin':
            account_money, _, _ = huobi_api.get_btc_withdraw_amount()
        else:
            account_money = huobi_api.get_spot_usdt_withdraw_amount()
    else:
        ...
    return account_money


# 用户的红利返佣比例
def user_rebate_rate(user_assets_type, user_rebate_type, start_time, middle_time, end_time):
    if user_assets_type == '散户':
        # 判断返佣类型
        if user_rebate_type == '普通':

            if start_time < time.time() <= middle_time:
                return 0.1
            elif middle_time < time.time() <= end_time:
                return 0.05
            else:
                return 0.05
        elif user_rebate_type == '商务':
            if start_time < time.time() <= middle_time:
                return 0.15
            elif middle_time < time.time() <= end_time:
                return 0.1
            else:
                return 0.05
        else:
            # TODO: 社群
            return 0.05
    else:
        # 判断返佣类型
        if user_rebate_type == '普通':

            if start_time < time.time() <= middle_time:
                return 0.03
            elif middle_time < time.time() <= end_time:
                return 0.02
            else:
                return 0.02
        elif user_rebate_type == '商务':
            if start_time < time.time() <= middle_time:
                return 0.05
            elif middle_time < time.time() <= end_time:
                return 0.02
            else:
                return 0.02
        else:
            # TODO: 社群
            return 0.02


# 发送提醒邮件的时间
def email_send_time(time_stamp):
    struct_time = time.localtime(time_stamp)
    format_time = time.strftime("%Y-%m-%d %X", struct_time)
    format_end_time = datetime.datetime.strptime(format_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)
    end_time = format_to_timestamp(format_end_time)
    return end_time


# 发邮件时间、次数缓存设置
def send_time_and_times(email_times, user_id):
    if email_times > 0:
        # 获取发送邮件的时间
        send_time = r.get(user_id)[1]
        # 时间到，发送邮件
        if time.time() > send_time:
            # TODO: 发邮件
            ...
        # 设置下次发送邮件的时间
        r.set(user_id, (email_times - 1, email_send_time(send_time)))


# 停止正在盈利的业务
def stop_contract(online_contract_list, user_id):
    for contract_obj_id in online_contract_list:
        # 查询列表中正在进行的协议对象
        contract_obj = contract_table.find_one({"_id": contract_obj_id})
        # 该协议的本位
        cash_mode = contract_obj['本位']
        # 该协议的交易所类型
        exchange = contract_obj['交易所']
        # api
        api = contract_obj['api']
        access_key = api['access_key']
        secret_key = api['secret_key']
        huobi_api = HuobiAPI(ACCESS_KEY=access_key, SECRET_KEY=secret_key)
        # 结算时资金和时间 [{"start_amount":本金, "end_amount":结算完金额, "ts":("start", "end")},{"start_amount":本金, "end_amount":结算完金额, "ts":("start", "end")}]
        capital_and_time = contract_obj["结算时资金和时间"]
        # 上次结算完的金额
        previous_assets = capital_and_time[-1]['end_amount']
        # 当前该协议中的资金（btc或usdt）
        account_money = account_assets(exchange, cash_mode, huobi_api)
        if account_money > previous_assets:
            # user_table.update_one({"_id": user_id},
            #                       {"$push": {"停止的协议列表": contract_obj_id}, "$pull": {"正在进行的协议列表": contract_obj_id}})
            user_table.update_one({"_id": user_id}, {"$pull": {"正在进行的协议列表": contract_obj_id}})
            contract_table.update_one({"_id": contract_obj_id}, {"$set": {'__启动停止(保证金用)__': 0}})


def timestamp_to_format(timestamp):
    struct_time = time.localtime(timestamp)
    format_time = time.strftime("%Y-%m-%d %X", struct_time)
    return format_time


def after_one_day(timestamp):
    struct_time = time.localtime(timestamp)
    format_time = time.strftime("%Y-%m-%d %X", struct_time)
    format_end_time = datetime.datetime.strptime(format_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=24)
    end_time = format_to_timestamp(format_end_time)
    return end_time


# 当前量化的盈利情况
def real_time_contract_profit(exchange, cash_mode, huobi_api, previous_assets):
    real_time_money = account_assets(exchange, cash_mode, huobi_api)
    real_time_profit = real_time_money - previous_assets
    return real_time_profit


def func():

    count = 0
    while page_size * count < user_info_num:
            # 每次查询5个用户进行分析
            for user_obj in user_table.find({}).limit(page_size).skip(page_size * count):
                online_contract_list = user_obj['正在进行的协议列表']  # type: list
                user_id = user_obj['_id']
                user_email = user_obj['email']
                user_type = user_obj['资金量类型']
                user_bond = user_obj['用户实际可用保证金']
                superior_user_id = user_obj['上级邀请人id']
                give_company_profit = user_obj['累计提供给平台的盈利']
                # stop_contract_list = user_obj['停止的协议列表']  # type: list
                owe_superior =0
                if user_obj['亏欠金额']['has_super']:
                    owe_superior = user_obj['亏欠金额'][superior_user_id]
                owe_company = user_obj['亏欠金额']['company']
                owe_money = owe_superior + owe_company

                # 判断正在进行的协议是否过期，得到最新的正在进行的协议列表
                if online_contract_list:
                    for contract_obj_id in online_contract_list:
                        # 查询列表中正在进行的协议对象
                        contract_obj = contract_table.find_one({"_id": contract_obj_id})
                        # 协议结束时间
                        contract_end_time = contract_obj['合同结束时间']
                        # 1.判断协议是否过期
                        if time.time() > contract_end_time:
                            online_contract_list.remove(contract_obj_id)
                            # 查询列表中正在进行的协议对象
                            contract_obj = contract_table.find_one({"_id": contract_obj_id})
                            # 该协议的本位
                            cash_mode = contract_obj['本位']
                            # 该协议的交易所类型
                            exchange = contract_obj['交易所']
                            # api
                            api = contract_obj['api']
                            access_key = api['access_key']
                            secret_key = api['secret_key']
                            huobi_api = HuobiAPI(ACCESS_KEY=access_key, SECRET_KEY=secret_key)
                            # 正在进行的协议的分成比例
                            divide_rate = contract_obj['分成比例']  # type: str
                            # 结算时资金和时间 [{"start_amount":本金, "end_amount":结算完金额, "ts":("start", "end")},{"start_amount":本金, "end_amount":结算完金额, "ts":("start", "end")}]
                            capital_and_time = contract_obj["结算时资金和时间"]
                            # 上次结算时时间
                            previous_time = capital_and_time[-1]['ts'][1]
                            # 上次结算完的金额
                            previous_assets = capital_and_time[-1]['end_amount']
                            # 当前协议的盈利
                            real_time_profit = real_time_contract_profit(exchange, cash_mode, huobi_api,
                                                                         previous_assets)
                            # 判断该协议是否盈利
                            ## 结算时该协议中资金
                            account_money = account_assets(exchange, cash_mode, huobi_api)
                            if account_money >= previous_assets:
                                # TODO: 盈利了
                                user_occupy = int(divide_rate.split(':')[0])
                                us_occupy = int(divide_rate.split(":")[1])
                                us_rate = us_occupy / (user_occupy + us_occupy)
                                # 利润
                                profit = account_money - previous_assets
                                ### 3.1.1 我们和该客户邀请人一共的利润分成
                                if cash_mode == "bitcoin":
                                    us_profit = profit * us_rate * huobi_api.get_spot_btcusdt_price()
                                else:
                                    us_profit = profit * us_rate
                                ### 3.1.2、判断用户实际可用保证金是否足够扣除
                                # 保证金足够
                                if user_bond >= us_profit:
                                    # 扣除分成后此时用户的保证金
                                    now_user_bond = user_bond - us_profit
                                    if superior_user_id:
                                        # 查询上级邀请人
                                        superior_user_obj = user_table.find_one({"_id": superior_user_id})
                                        # 上级邀请人返佣类型
                                        superior_rebate_type = superior_user_obj['返佣类型']
                                        # 上级资金量类型
                                        superior_assets_type = superior_user_obj['资金量类型']
                                        # 红利返佣3个时间点
                                        start_time = superior_user_obj['账户红利返佣时间'][0]
                                        middle_time = superior_user_obj['账户红利返佣时间'][1]
                                        end_time = superior_user_obj['账户红利返佣时间'][2]
                                        # 上级用户的返佣比例
                                        superior_rebate_rate = user_rebate_rate(superior_assets_type,
                                                                                superior_rebate_type,
                                                                                start_time, middle_time, end_time)
                                        # 上级用户分得的利润
                                        superior_user_profit = profit * superior_rebate_rate
                                        # 公司分得的利润
                                        company_profit = us_profit - superior_user_profit
                                        # 该用户已为上级邀请人带来的利润
                                        created_profit = user_table.find_one({'_id': superior_user_id})['下级邀请人'][
                                            user_id]
                                        # 更新上级用户表
                                        user_table.update_one({'_id': superior_user_id}, {
                                            "$set": {"下级邀请人.user_id": created_profit + superior_user_profit}, '$push': {
                                                "保证金缴纳记录": {"ts": timestamp_to_format(time.time()),
                                                            "amount": superior_user_profit, "source": "划转"}}})

                                        # 更新该用户表

                                        user_table.update_one({'_id': user_id}, {"$set": {"用户实际可用保证金": now_user_bond,
                                                                                          "累计提供返佣": created_profit + superior_user_profit,
                                                                                          "累计提供给平台的盈利": company_profit + give_company_profit,
                                                                                          "现有盈利需要保证金数量": online_contract_assets(
                                                                                              online_contract_list) * 0.05}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                                    else:
                                        # 更新该用户表
                                        user_table.update_one({'_id': user_id}, {"$set": {"用户实际可用保证金": now_user_bond,
                                                                                          "累计提供给平台的盈利": us_profit + give_company_profit,
                                                                                          "现有盈利需要保证金数量": online_contract_assets(
                                                                                              online_contract_list) * 0.05}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                                else:
                                    now_user_bond = user_bond - us_profit
                                    # TODO:保证金不够扣
                                    if superior_user_id:
                                        # 查询上级邀请人
                                        superior_user_obj = user_table.find_one({"_id": superior_user_id})
                                        # 上级邀请人返佣类型
                                        superior_rebate_type = superior_user_obj['返佣类型']
                                        # 上级资金量类型
                                        superior_assets_type = superior_user_obj['资金量类型']
                                        # 红利返佣3个时间点
                                        start_time = superior_user_obj['账户红利返佣时间'][0]
                                        middle_time = superior_user_obj['账户红利返佣时间'][1]
                                        end_time = superior_user_obj['账户红利返佣时间'][2]
                                        # 上级用户的返佣比例
                                        superior_rebate_rate = user_rebate_rate(superior_assets_type,
                                                                                superior_rebate_type,
                                                                                start_time, middle_time, end_time)
                                        # 上级用户应分得的利润
                                        superior_user_profit = profit * superior_rebate_rate
                                        # 公司应分得的利润
                                        company_profit = us_profit - superior_user_profit
                                        # 更新该用户表
                                        user_table.update_one({'_id': user_id}, {
                                            "$set": {"用户实际可用保证金": now_user_bond,"现有盈利需要保证金数量": online_contract_assets(online_contract_list) * 0.05,
                                                     "亏欠金额": {"has_super":True, superior_user_id: superior_user_profit,
                                                              "company": company_profit}},"$pull": {"正在进行的协议列表": contract_obj_id}, "$push": {"已完成协议列表": contract_obj_id}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                                    else:
                                        # 更新该用户表
                                        user_table.update_one({'_id': user_id}, {
                                            "$set": {"现有盈利需要保证金数量": online_contract_assets(online_contract_list) * 0.05,
                                                     "亏欠金额": {"has_super": False,
                                                              "company": us_profit}},"$pull": {"正在进行的协议列表": contract_obj_id}, "$push": {"已完成协议列表": contract_obj_id}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                            else:
                                # TODO: 结算流程

                                # TODO: 亏本了
                                # 更新该用户表
                                user_table.update_one({'_id': user_id}, {
                                    "$set": {"现有盈利需要保证金数量": online_contract_assets(online_contract_list) * 0.05}, "$pull": {"正在进行的协议列表": contract_obj_id}, "$push": {"已完成协议列表": contract_obj_id}})
                                contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                    "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                 "ts": (previous_time, time.time())}}})

                            contract_table.update_one({"_id": contract_obj_id}, {"$set": {'__启动停止(保证金用)__': 0}})

                # 判断已经停止的协议是否过期
                # if stop_contract_list:
                #     for contract_obj_id in stop_contract_list:
                #         # 查询列表中正在进行的协议对象
                #         contract_obj = contract_table.find_one({"_id": contract_obj_id})
                #         # 协议结束时间
                #         contract_end_time = contract_obj['合同结束时间']
                #         # 1.判断协议是否过期
                #         if time.time() > contract_end_time:
                #             user_table.update_one({"_id": user_id}, {"$pull": {"停止的协议列表": contract_obj_id}})
                #             user_table.update_one({"_id": user_id}, {"$push": {"已完成协议列表": contract_obj_id}})
                #         stop_contract_list.remove(contract_obj_id)
                # new_online_contract_list = online_contract_list + stop_contract_list
                # 判断用户正在进行的协议列表和已经停止的协议列表中所有协议的资金量*0.05是否大于保证金bond

                # if new_online_contract_list:
                #     all_contract_assets = online_contract_assets(new_online_contract_list)
                #     if user_bond > all_contract_assets * 0.05:
                #         online_contract_list.extend(stop_contract_list)
                # 判断用户正在进行的协议列表中所有协议的资金量*0.05是否大于保证金bond
                # if online_contract_list:
                #     all_contract_assets = online_contract_assets(online_contract_list)
                #     if user_bond > all_contract_assets * 0.05:
                #         online_contract_list.extend(stop_contract_list)
                # 判断保证金是否大于正在进行协议总资产的5%

                # 判断用户的保证金是否大于5%
                if online_contract_list:
                    # 用户正在进行的协议的总资产
                    user_all_assets = online_contract_assets(online_contract_list)
                    # 2.实际可用保证金/正在进行量化的协议的总资产
                    bond_rate = user_bond / user_all_assets

                    print(bond_rate)
                    if 0.02 <= bond_rate < 0.05:
                        # TODO:保证金不足  发邮件
                        send_prompt_msg(user_email)
                    elif 0.01 <= bond_rate < 0.02:
                        # TODO:保证金不足  发邮件
                        send_prompt_msg(user_email)
                        # 设置下次发送邮件的时间
                    elif bond_rate < 0.01:
                        # TODO:保证金不足  发邮件
                        print(666666666666666666666)
                        send_prompt_msg(user_email)


                # 先判断该用户是否欠钱
                if owe_money:
                    if user_bond > owe_money:
                        user_bond = user_bond - owe_money

                        # 判断该用户有无上级邀请人
                        if superior_user_id:
                            # 该用户已为上级邀请人带来的利润
                            created_profit = user_table.find_one({'_id': superior_user_id})['下级邀请人'][user_id]
                            user_table.update_one({"_id": superior_user_id},
                                                  {"$set": {"下级邀请人.user_id": created_profit + owe_superior}, '$push': {
                                                      "保证金缴纳记录": {"ts": timestamp_to_format(time.time()),
                                                                  "amount": owe_superior, "source": "划转"}}})
                            # 更新该用户表
                            if online_contract_list:
                                need_money = online_contract_assets(online_contract_list) * 0.05
                            else:
                                need_money = 0
                            user_table.update_one({'_id': user_id}, {
                                "$set": {"用户实际可用保证金": user_bond, "累计提供返佣": created_profit + owe_superior,
                                         "累计提供给平台的盈利": owe_company + give_company_profit,
                                         "现有盈利需要保证金数量": need_money,
                                         "亏欠金额": {"has_super":True, superior_user_id: 0, "company": 0}}})
                            r.delete(user_id)
                        else:
                            # 更新该用户表
                            if online_contract_list:
                                need_money = online_contract_assets(online_contract_list) * 0.05
                            else:
                                need_money = 0
                            user_table.update_one({'_id': user_id}, {
                                "$set": {"用户实际可用保证金": user_bond,
                                         "累计提供给平台的盈利": owe_company + give_company_profit,
                                         "现有盈利需要保证金数量": need_money,
                                         "亏欠金额": {"has_super": False, "company": 0}}})
                            r.delete(user_id)
                    else:
                        if r.exists(user_id):
                            # 获取发送邮件的次数
                            email_times = r.get(user_id)[0]
                            # 查看发邮件的时间
                            send_time = r.get(user_id)[1]
                            # 提醒次数未达到3次
                            if email_times > 0:
                                # 发邮件的时间到了
                                if time.time() > send_time:
                                    send_prompt_msg(user_email)
                                    # 设置下次发送邮件的时间
                                    r.set(user_id, (email_times - 1, email_send_time(send_time)))
                            else:
                                # 欠款时间超过24小时, 停止所有正在盈利的协议
                                stop_contract(online_contract_list, user_id)
                                r.delete(user_id)
                        else:
                            r.set(user_id, (3, time.time()))

                if online_contract_list:
                    for contract_obj_id in online_contract_list:
                        # 查询列表中正在进行的协议对象
                        contract_obj = contract_table.find_one({"_id": contract_obj_id})
                        # 该协议的本位
                        cash_mode = contract_obj['本位']
                        # 该协议的交易所类型
                        exchange = contract_obj['交易所']
                        # api
                        api = contract_obj['api']
                        access_key = api['access_key']
                        secret_key = api['secret_key']
                        huobi_api = HuobiAPI(ACCESS_KEY=access_key, SECRET_KEY=secret_key)
                        # 正在进行的协议的分成比例
                        divide_rate = contract_obj['分成比例']  # type: str
                        # 结算时资金和时间 [{"start_amount":本金, "end_amount":结算完金额, "ts":("start", "end")},{"start_amount":本金, "end_amount":结算完金额, "ts":("start", "end")}]
                        capital_and_time = contract_obj["结算时资金和时间"]
                        # 上次结算时时间
                        previous_time = capital_and_time[-1]['ts'][1]
                        # 上次结算完的金额
                        previous_assets = capital_and_time[-1]['end_amount']
                        # 当前协议的盈利
                        real_time_profit = real_time_contract_profit(exchange, cash_mode, huobi_api, previous_assets)
                        # 实时更新当前量化的盈亏情况
                        contract_table.update_one({'_id': contract_obj_id}, {"$set": {"量化盈亏": real_time_profit}})
                        # 3.判断是否到结算日期
                        later_time = ord_settle_time(user_type, previous_time)
                        ## 3.1、到结算日期
                        if time.time() > later_time:
                            # 判断该协议是否盈利
                            ## 结算时该协议中资金
                            account_money = account_assets(exchange, cash_mode, huobi_api)
                            if account_money >= previous_assets:
                                # TODO: 盈利了
                                user_occupy = int(divide_rate.split(':')[0])
                                us_occupy = int(divide_rate.split(":")[1])
                                us_rate = us_occupy / (user_occupy + us_occupy)
                                # 利润
                                profit = account_money - previous_assets
                                ### 3.1.1 我们和该客户邀请人一共的利润分成
                                if cash_mode == "bitcoin":
                                    us_profit = profit * us_rate * huobi_api.get_spot_btcusdt_price()
                                else:
                                    us_profit = profit * us_rate
                                ### 3.1.2、判断用户实际可用保证金是否足够扣除
                                # 保证金足够
                                if user_bond >= us_profit:
                                    # 扣除分成后此时用户的保证金
                                    now_user_bond = user_bond - us_profit
                                    if superior_user_id:
                                        # 查询上级邀请人
                                        superior_user_obj = user_table.find_one({"_id": superior_user_id})
                                        # 上级邀请人返佣类型
                                        superior_rebate_type = superior_user_obj['返佣类型']
                                        # 上级资金量类型
                                        superior_assets_type = superior_user_obj['资金量类型']
                                        # 红利返佣3个时间点
                                        start_time = superior_user_obj['账户红利返佣时间'][0]
                                        middle_time = superior_user_obj['账户红利返佣时间'][1]
                                        end_time = superior_user_obj['账户红利返佣时间'][2]
                                        # 上级用户的返佣比例
                                        superior_rebate_rate = user_rebate_rate(superior_assets_type,
                                                                                superior_rebate_type,
                                                                                start_time, middle_time, end_time)
                                        # 上级用户分得的利润
                                        superior_user_profit = profit * superior_rebate_rate
                                        # 公司分得的利润
                                        company_profit = us_profit - superior_user_profit
                                        # 该用户已为上级邀请人带来的利润
                                        created_profit = user_table.find_one({'_id': superior_user_id})['下级邀请人'][
                                            user_id]
                                        # 更新上级用户表
                                        user_table.update_one({'_id': superior_user_id}, {
                                            "$set": {"下级邀请人.user_id": created_profit + superior_user_profit}, '$push': {
                                                "保证金缴纳记录": {"ts": timestamp_to_format(time.time()),
                                                            "amount": superior_user_profit, "source": "划转"}}})

                                        # 更新该用户表
                                        user_table.update_one({'_id': user_id}, {"$set": {"用户实际可用保证金": now_user_bond,
                                                                                          "累计提供返佣": created_profit + superior_user_profit,
                                                                                          "累计提供给平台的盈利": company_profit + give_company_profit,
                                                                                          "现有盈利需要保证金数量": online_contract_assets(
                                                                                              online_contract_list) * 0.05}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                                    else:
                                        # 更新该用户表
                                        user_table.update_one({'_id': user_id}, {"$set": {"用户实际可用保证金": now_user_bond,
                                                                                          "累计提供给平台的盈利": us_profit + give_company_profit,
                                                                                          "现有盈利需要保证金数量": online_contract_assets(
                                                                                              online_contract_list) * 0.05}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                                else:
                                    r.set(user_id, (3, time.time()))
                                    # TODO:保证金不够扣
                                    if superior_user_id:
                                        # 查询上级邀请人
                                        superior_user_obj = user_table.find_one({"_id": superior_user_id})
                                        # 上级邀请人返佣类型
                                        superior_rebate_type = superior_user_obj['返佣类型']
                                        # 上级资金量类型
                                        superior_assets_type = superior_user_obj['资金量类型']
                                        # 红利返佣3个时间点
                                        start_time = superior_user_obj['账户红利返佣时间'][0]
                                        middle_time = superior_user_obj['账户红利返佣时间'][1]
                                        end_time = superior_user_obj['账户红利返佣时间'][2]
                                        # 上级用户的返佣比例
                                        superior_rebate_rate = user_rebate_rate(superior_assets_type,
                                                                                superior_rebate_type,
                                                                                start_time, middle_time, end_time)
                                        # 上级用户应分得的利润
                                        superior_user_profit = profit * superior_rebate_rate
                                        # 公司应分得的利润
                                        company_profit = us_profit - superior_user_profit
                                        # 更新该用户表
                                        user_table.update_one({'_id': user_id}, {
                                            "$set": {"现有盈利需要保证金数量": online_contract_assets(online_contract_list) * 0.05,
                                                     "亏欠金额": {"has_super":True, superior_user_id: superior_user_profit,
                                                              "company": company_profit}}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                                    else:
                                        # 更新该用户表
                                        user_table.update_one({'_id': user_id}, {
                                            "$set": {"现有盈利需要保证金数量": online_contract_assets(online_contract_list) * 0.05,
                                                     "亏欠金额": {'has_super': False,
                                                              "company": us_profit}}})

                                        # TODO: 更新当前协议  “结算时资金和时间”字段
                                        contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                            "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                         "ts": (previous_time, time.time())}}})
                            else:
                            # TODO: 结算流程

                                # TODO: 亏本了
                                # 更新该用户表
                                user_table.update_one({'_id': user_id}, {
                                    "$set": {"现有盈利需要保证金数量": online_contract_assets(online_contract_list) * 0.05}})
                                contract_table.update_one({'_id': contract_obj_id}, {"$push": {
                                    "结算时资金和时间": {"start_amount": previous_assets, "end_amount": account_money,
                                                 "ts": (previous_time, time.time())}}})
            count += 1


func()
# while True:
#     func()
    # try:
    #     func()
    # except Exception as e:
    #     print(e)
    #     send_error_msg('xiaolang7421@163.com', str(e))
    #     break


