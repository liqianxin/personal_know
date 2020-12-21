#! /usr/bin/env python
# -*- coding:utf-8 -*-


'''
充币流程：
1、生成地址接口
通过这个接口给平台用户请求分配一个充值地址
2、用户向这个地址充值会通过交易回调接口将充值信息推送给平台，平台收到充值信息后对业务进行处理

提币流程：
1、提币接口，平台将用户提币信息通过这个接口将传给钱包，钱包审核后发送交易
2、钱包会通过交易回调接口将审核结果和交易结果分两次回调传个平台，平台根据回调信息对业务进行处理

网关服务器：
https://hk05-node.uduncloud.com （华南）

https://hk05-hk-node.uduncloud.com （香港）
'''
import hashlib
import random
import time
import requests
import json
import uuid


APIKEY = '85f9bcc7a69ac5fc2942571f9fe04ab3'
huanan_host = 'https://hk05-node.uduncloud.com'
hongkong_host = 'https://hk05-hk-node.uduncloud.com'
merchant_number = '302092'
callUrl = 'http://localhost:8000/callback/'
withdraw_url = ''


def withdraw(address, amount):
    '''提币'''
    # 验证用户提币地址的合法性
    res = check_address(address)
    if res['code'] !=200:
        return {'code': 201, 'message': '提币地址不合法'}
    body = [
        {
            "address": address,  # 用户自己填写的提币地址
            "amount": amount,
            "merchantId": merchant_number,
            "mainCoinType": "0",
            "coinType": "31",
            "callUrl": withdraw_url,
            "businessId": uuid.uuid4(),
            "memo": ""

        }
    ]
    url = '/mch/withdraw'
    return http_post(url, body)


def create_address():
    '''请求分配充值地址
    {'code': 200, 'data': {'coinType': 0, 'address': '1HCc5d6Zojsk9dyreMrrGXwg2zuSYT5Pks'}, 'message': 'SUCCESS'}
    '''
    body = [{
        'merchantId': merchant_number,
        'coinType': 0,
        'callUrl': callUrl
    }]
    url = '/mch/address/create'
    return http_post(url, body)


def check_address(address):
    '''校验地址的合法性'''
    url = '/mch/check/address'
    body = [{
        "merchantId": merchant_number,
        "mainCoinType": "0",
        "address": address
    }]
    return http_post(url, body)


def get_support_bitcoin():
    '''获取商户支持的币种信息'''
    body = {
        'merchantId': merchant_number,
        'showBalance': True
    }
    url = '/mch/support-coins'
    return http_post(url, body)


def create_sign(body_json, nonce, timestamp):
    '''create sign'''
    str_sign = str(body_json)+APIKEY+str(nonce)+str(timestamp)
    md = hashlib.md5(str_sign.encode('utf-8'))
    sign = md.hexdigest()
    return sign


def http_post(url, body):
    '''发起请求'''
    nonce = random.randint(100000, 999999)
    timestamp = time.time()
    body_json = json.dumps(body)
    data = {
        "timestamp": timestamp,
        "nonce": nonce,
        "sign": create_sign(body_json, nonce, timestamp),
        "body": body_json
    }
    header = {
        'Content-Type': 'application/json'
    }
    full_url = hongkong_host + url
    data_json = json.dumps(data)
    res = requests.post(full_url, headers=header, data=data_json)
    return res.json()


a = check_address('1111')
print(a)