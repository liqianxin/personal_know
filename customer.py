# 只能是币本位, 没做金本位的去 币本位交割合约市场 卖空的逻辑
import time, pymongo, traceback, inspect, redis, pickle, smtplib, os, logging, random, math
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId
from email.mime.text import MIMEText
from sdk.huobi_sdk import api_key_get, api_key_post, http_get_request
from sdk.HuobiDMService import HuobiDM


def get_document():
    doc = customer_register_mongodb['users'].find_one({'_id': customer_object_id})
    return doc


def get_document_field(field):
    assert type(field) == str
    value = customer_register_mongodb['users'].find_one({'_id': customer_object_id}, projection=[field])[field]
    return value


def get_document_fields(fields):
    assert type(fields) == list or type(fields) == tuple
    values_dict = customer_register_mongodb['users'].find_one({'_id': customer_object_id}, projection=fields)
    fields = set(fields)
    values_dict = {k: v for k, v in values_dict.items() if k in fields}
    return values_dict


def set_document_field(field, value):
    customer_register_mongodb['users'].update_one({'_id': customer_object_id}, {'$set': {field: value}})


# 后面的 customer 的服务器移仓, 一边平当周的, 一边开次季的, 当周的不管是浮亏还是浮盈, 次季都是按照初始资金量开单

# 金本位: 当周的全部平掉(因为 portfolio 是 0 仓位), 当季的按照 portfolio 的仓位百分比 * 初始资金量(USD)来计算可以用多少资金量开单, 再用资金量 / 当季的价格, 获取开的 BTC 的数量, 再用用每张0.01BTC 来计算张数

# 币本位: 当周的全部平掉(因为 portfolio 是 0 仓位), 当季的按照 portfolio 的仓位百分比 * 初始资金量(BTC)来计算可以用多少资金量(BTC)开单, 再用资金量 / 当季的价格, 获取开的 USD 的数量, 再用用每张 100USD 来计算张数

################################################################################################################
CUSTOMER_MONGODB_ID = str(__file__.split('.')[0].split('customer_')[1])
customer_object_id = ObjectId(CUSTOMER_MONGODB_ID)
MACHINE_NAME = os.environ.get('NAME', 'unset_name')
_print = print
print = lambda *args: _print(f"{ts2str(time.time())} | {' | '.join([str(el) for el in args])}")
lineno = lambda: inspect.currentframe().f_back.f_lineno
ts2str = lambda ts: time.strftime('%Y/%m/%d - %H:%M:%S', time.gmtime(ts + 8 * 3600))
str2ts = lambda string: int(time.mktime(time.strptime(string, '%Y/%m/%d - %H:%M:%S')))
class Password: pass

password = pickle.load(open('/root/.customer_password_file', 'rb'))

r = redis.Redis(
    host=password.portfolio_host,
    port=password.portfolio_redis_port,
    password=password.portfolio_redis_password)
ps = r.pubsub()

customer_panel_mongodb = pymongo.MongoClient(host=password.customer_panel_mongo_host, port=password.customer_panel_mongo_port)['panel']
customer_panel_mongodb.authenticate(password.customer_panel_mongo_username, password.customer_panel_mongo_password)

customer_register_mongodb = pymongo.MongoClient(host=password.customer_register_mongo_host, port=password.customer_register_mongo_port)['register']
customer_register_mongodb.authenticate(password.customer_register_mongo_username, password.customer_register_mongo_password)
del password

logging.basicConfig(
    filename=f'{str(CUSTOMER_MONGODB_ID)}.log',
    format=f'%(asctime)s | %(lineno)d | %(levelname)s | %(funcName)s | {CUSTOMER_MONGODB_ID} | {MACHINE_NAME} | %(message)s\n',
    datefmt='%Y/%m/%d - %H:%M:%S',
    level=20)

# api settings
spot_domain = 'https://api.huobi.pro'
huobidm_domain = 'https://api.hbdm.com'
ACCESS_KEY = get_document_field('__huobi_access_key__')
SECRET_KEY = get_document_field('__huobi_secret_key__')
dm = HuobiDM(huobidm_domain, ACCESS_KEY, SECRET_KEY)


class HuobiAPI:
    def __init__(self, ACCESS_KEY, SECRET_KEY):
        self.ACCESS_KEY = ACCESS_KEY
        self.SECRET_KEY = SECRET_KEY
        res = self.ensure_status_ok(api_key_get, (spot_domain, '/v1/account/accounts', {}, self.ACCESS_KEY, self.SECRET_KEY), init_class=True)
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
        res = self.ensure_status_ok(api_key_post, [spot_domain, '/v1/order/orders/batchCancelOpenOrders', {}, api.ACCESS_KEY, api.SECRET_KEY])
        return res

    def spot_place_order(self, params):
        res = api_key_post(spot_domain, '/v1/order/orders/place', params, api.ACCESS_KEY, api.SECRET_KEY)
        return res

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

    @staticmethod
    def _check_sub_account():
        """{'status': 'error', 'err_code': 1018, 'err_msg': 'Main account doesnt exist.', 'ts': 1606025162666}"""
        """{'status': 'ok', 'data': [{'sub_uid': 136867614, 'list': [{'symbol': 'BSV', 'margin_balance': 0, 'liquidation_price': None, 'risk_rate': None}, {'symbol': 'BCH', 'margin_balance': 0,"""
        c = 1
        while 1:
            try:
                res = api_key_post(huobidm_domain, '/api/v1/contract_sub_account_list', {}, ACCESS_KEY , SECRET_KEY)
                if 'status' in res:
                    return res
            except:
                if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                    logging.warning(f'check_sub_account方法第{c - 1}次报错, {traceback.format_exc()}')
                    my_email(f'lineno: {lineno()}, check_sub_account方法第{c - 1}次报错', traceback.format_exc())
            c += 1
            time.sleep(1)

    def get_order_residual(self, order_id):
        res = self.get_contract_order_info(order_id)
        volume = int(res['data'][0]['volume'])
        trade_volume = int(res['data'][0]['trade_volume'])
        residual = volume - trade_volume
        return residual, volume , trade_volume

    @staticmethod
    def get_contract_order_info(order_id):
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
                res = dm.get_contract_order_info(symbol='BTC', order_id=order_id)
                if res['status'] == 'ok' and len(res['data']) == 1:
                    return res
            except:
                if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                    logging.warning(f'get_contract_order_info方法第{c - 1}次报错, {traceback.format_exc()}')
                    my_email(f'lineno: {lineno()}, get_contract_order_info方法第{c - 1}次报错', traceback.format_exc())
            c += 1
            time.sleep(1)

    @staticmethod
    def place_order(zhang, direction, offset, contract_type):
        """
        {'status': 'ok', 'data': {'order_id': 779776450755874816, 'order_id_str': '779776450755874816'}, 'ts': 1605954793408}

        全部以对手价下单
        开平方向
        开多：买入开多(direction用buy、offset用open)
        平多：卖出平多(direction用sell、offset用close)
        开空：卖出开空(direction用sell、offset用open)
        平空：买入平空(direction用buy、offset用close)
        """
        """下单返回的信息有问题, res: {'status': 'error', 'err_code': 1233, 'err_msg': 'High leverage is not enabled (Please sign in the APP or web with your main account to agree to the High-Leverage Agreement)', 'ts': 1606893213213}
        """
        symbol = 'BTC'

        lever_rate = 100
        order_price_type = 'opponent'
        try:
            """res: {'status': 'error', 'err_code': 1233, 'err_msg': 'High leverage is not enabled (Please sign in the APP or web with your main account to agree to the High-Leverage Agreement)', 'ts': 1606893213213}"""
            res = dm.send_contract_order(
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
        if res['status'] == 'error' and res['err_code'] == 1233:
            logging.error(f'place_order response: {res}')
            raise Exception
        return res

    @staticmethod
    def get_exchange_position(return_detail=False):
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
                res = dm.get_contract_position_info("BTC")
                if res['status'] == 'ok':
                    long_zhang = 0
                    short_zhang = 0
                    if len(res['data']) > 2:
                        logging.info(f'{res}')

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
                if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                    logging.warning(f'get_exchange_position方法第{c - 1}次报错, {traceback.format_exc()}')
                    my_email(f'lineno: {lineno()}, get_exchange_position方法第{c - 1}次报错', traceback.format_exc())
            c += 1
            time.sleep(1)

    @staticmethod
    def ensure_status_ok(fun, params_list, init_class=False):
        def check_status_ok(res):
            if res['status'] == 'ok':
                return True
            else:
                return False

        c = 0
        res = f'lineno: {lineno()}, 未生成信息'
        while 1:
            try:
                res = fun(*params_list)
                if check_status_ok(res):
                    return res
            except:
                pass

            if init_class:
                logging.warning(res)
            time.sleep(3)
            c += 1
            if c > 5 and init_class:
                raise Exception


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
        futures_btc_info = dm.get_contract_account_info("BTC")['data'][0]
        futures_btc = futures_btc_info['withdraw_available']
        have_position = futures_btc_info['margin_position']
        have_position = True if have_position else False

        return float(spot_btc), float(futures_btc), have_position

    @staticmethod
    def have_position():
        futures_btc_info = dm.get_contract_account_info("BTC")['data'][0]
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
        res = api_key_post(spot_domain, channel, params, self.ACCESS_KEY, self.SECRET_KEY)
        return res

    @staticmethod
    def cancel_all_order():
        """{'data': {'errors': [], 'successes': '779774592629473280,779774872988471296'},
         'status': 'ok',
         'ts': 1605954526488}"""
        c = 1
        while 1:
            try:
                res = dm.cancel_all_contract_order(symbol='BTC')
                if (res['err_msg'] == 'No orders to cancel.') or (res['status'] == 'ok' and res['data']['errors'] == []):
                    return res
            except:
                if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                    logging.warning(f'取消所有订单的方法第{c - 1}次报错, {traceback.format_exc()}')
                    my_email(f'lineno: {lineno()}, 取消所有订单的方法第{c - 1}次报错', traceback.format_exc())
            c += 1
            time.sleep(1)

    @staticmethod
    def get_quarter_price(return_dict=False):
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
                res = dm.get_contract_depth(symbol='BTC_CQ', type='step6')
                if res['status'] == 'ok':
                    bid = res['tick']['bids'][0][0]
                    ask = res['tick']['asks'][0][0]
                    if not return_dict:
                        price = (bid + ask) / 2
                        return price
                    else:
                        return {'bid': bid, 'ask': ask}
            except:
                if c > 1 and math.log(c, 10) % 1 == 0:  # c == 10, 100, 1000, 10000, 100000
                    logging.warning(f'get_quarter_price方法第{c - 1}次报错, {traceback.format_exc()}')
                    my_email(f'lineno: {lineno()}, get_quarter_price方法第{c - 1}次报错', traceback.format_exc())
            c += 1
            time.sleep(0.5)


def my_email(title, content, email_ts=[0]):
    title += f'CUSTOMER_MONGODB_ID: {CUSTOMER_MONGODB_ID} | MACHINE_NAME: {MACHINE_NAME}'
    content += f'CUSTOMER_MONGODB_ID: {CUSTOMER_MONGODB_ID} | MACHINE_NAME: {MACHINE_NAME}'
    def _163_mail(title, content):
        if int(get_document_field('send_email')):
            receiver_list = ['1132300949@qq.com', 'liuningqian2413@msn.com', '24630638@qq.com', 'qqddbxx@163.com']
        else:
            receiver_list = ['1132300949@qq.com', 'liuningqian2413@msn.com']
        username = '15506230887@163.com'
        passwd = '1ppwmdkbdlmibafh'
        mail_host = 'smtp.163.com'
        port = 465
        smtp = smtplib.SMTP_SSL(mail_host, port=port)
        smtp.login(username, passwd)
        for recv in receiver_list:
            try:
                msg = MIMEText(content)
                msg['Subject'] = title
                msg['From'] = username
                msg['To'] = recv
                smtp.sendmail(username, recv, msg.as_string())
            except smtplib.SMTPDataError:
                try:
                    content += """
                    这是我后来加上去的正文, 防止被163退回, 这是来自 163 的邮件. """
                    msg = MIMEText(content)
                    msg['Subject'] = title
                    msg['From'] = username
                    msg['To'] = recv
                    smtp.sendmail(username, recv, msg.as_string())
                except smtplib.SMTPDataError:
                    title += """ | 这是我后来加上去的标题, 防止被163退回"""
                    msg = MIMEText(content)
                    msg['Subject'] = title
                    msg['From'] = username
                    msg['To'] = recv
                    smtp.sendmail(username, recv, msg.as_string())
            except:
                try:
                    content += """
                        这是我后来加上去的正文, 防止被163退回, 这是来自 163 的邮件. """
                    title += """ | 这是我后来加上去的标题, 防止被163退回"""
                    msg = MIMEText(content)
                    msg['Subject'] = title
                    msg['From'] = username
                    msg['To'] = recv
                    smtp.sendmail(username, recv, msg.as_string())
                except:
                    pass
        smtp.quit()

    if time.time() > email_ts[0] + 60 * 5:
        email_ts[0] = time.time()
        try:
            try:
                executor.submit(_163_mail, title, content)
            except:
                pass
        except:
            pass
    else:
        logging.critical(f'email_send: False or less than 5 min, title: {title} , content: {content}')


class Lock:
    def __init__(self):
        self.locked1 = False
        self.locked2 = False

    def acquire(self):
        c = 0
        start_ts = time.time()

        while self.locked1:
            c += 1
            if c >= 300 and c % 100 == 0:  # 等待超过 30 秒, 每 10 秒需要打印 logging
                logging.warning(f'lock1 已等待{time.time() - start_ts}秒')
            time.sleep(random.random() / 5)
        self.locked1 = True

        time.sleep(random.random() / 100)

        while self.locked2:
            c += 1
            if c >= 300 and c % 100 == 0:  # 等待超过 30 秒, 每 10 秒需要打印 logging
                logging.warning(f'lock2 已等待{time.time() - start_ts}秒')
            time.sleep(random.random() / 5)
        self.locked2 = True


    def release(self):
        if not self.locked1:
            logging.warning(f'lock1 release的时候已经解锁了, 查原因')
        if not self.locked2:
            logging.warning(f'lock2 release的时候已经解锁了, 查原因')
        self.locked1 = False
        self.locked2 = False


def manual_change_portfolio():
    def changed():
        portfolio = get_document_field('手动调整仓位')
        for v in portfolio.values():
            if v != 'unset':
                portfolio_convert_to_float = {}
                for k, v in portfolio.items():
                    try:
                        portfolio_convert_to_float[k] = float(v)
                    except:
                        portfolio_convert_to_float[k] = 'unset'
                return True, portfolio_convert_to_float
        return False, portfolio

    def change_back(changed_portfolio):
        keys = changed_portfolio.keys()
        unchanged_portfolio = {k: 'unset' for k in keys}
        set_document_field('手动调整仓位', unchanged_portfolio)

    def changed_portfolio2target_portfolio(changed_portfolio):
        now_portfolio = get_document_field('__portfolio__')
        for k, v in changed_portfolio.items():
            if v != 'unset':
                now_portfolio[k] = v
        return now_portfolio

    try:
        while 1:
            try:
                is_changed, changed_portfolio = changed()
                if not is_changed:
                    time.sleep(3)
                    continue
                else:
                    change_back(changed_portfolio)
            except:
                logging.error(f'ERROR: {traceback.format_exc()}')
                time.sleep(1)
                continue

            lock.acquire()

            try:
                checked = False
                for _ in range(60):
                    time.sleep(1)
                    is_changed, changed_portfolio2 = changed()
                    if is_changed:
                        change_back(changed_portfolio2)
                        if changed_portfolio == changed_portfolio2:
                            checked = True
                        break

                if checked:
                    targ_portfolio = changed_portfolio2target_portfolio(changed_portfolio)
                    targ_position = targ_portfolio['btc_quarter']
                    now_portfolio = get_document_field('__portfolio__')

                    change_position_to_target_position(now_portfolio=now_portfolio, targ_portfolio=targ_portfolio)

                    now_portfolio['btc_quarter'] = targ_position
                    set_document_field('__portfolio__', now_portfolio)
            except:
                lock.release()
                logging.error(f'ERROR: {traceback.format_exc()}')
                time.sleep(1)
                continue

            lock.release()

    except:
        logging.error(f'ERROR: {traceback.format_exc()}')


def customer():
    def get_publish_portfolio():
        for item in ps.listen():
            if item['type'] == 'message':
                publish_portfolio = pickle.loads(item['data'])
                yield publish_portfolio

    def ts_count_warning(ts_delta, count_delta, ts_max_delta):
        if ts_delta > 0.5:
            logging.warning(f'延迟了{ts_delta}秒接收到redis, ts_max_delta: {ts_max_delta}')
        if count_delta != 1:
            logging.critical(f'redis的信息可能有遗漏: count_delta: {count_delta}, ts_max_delta: {ts_max_delta}')

    def transfer_to_targ_portfolio(publish_portfolio):
        fields = ['spot', 'btc_this_week', 'btc_next_week', 'btc_quarter', 'btc_bi_quarter', 'btc_swap', 'usdt_swap']
        # 不直接用 publish_portfolio 的 keys, 是为了去除 ts, count 和 meth 等 keys
        customer_portfolio = {k: publish_portfolio[k][0] for k in fields}
        return customer_portfolio

    publish_portfolio_generator = get_publish_portfolio()
    prev_count = None
    while 1:
        try:
            for publish_portfolio in publish_portfolio_generator:
                # 对 redis 的发布订阅消息的质量进行验证
                ts_delta = time.time() - publish_portfolio.get('ts')
                now_count = publish_portfolio.get('count')
                count_delta = now_count - (prev_count if prev_count is not None else (now_count - 1))
                prev_count = now_count
                ts_max_delta = publish_portfolio.get('ts_max_delta', 10)
                random_sleep_multiplier_place_order = publish_portfolio.get('random_sleep_multiplier_place_order', 120)

                lock.acquire()

                if ts_delta > ts_max_delta:  # 超过 1 分钟的都忽略, 如果是中频, 超过10 秒都忽略
                    lock.release()
                    ts_count_warning(ts_delta, count_delta, ts_max_delta)
                    continue  # 超过 1 小时的信号不再买入, 比如用户保证金没缴纳, 超过 1 小时这些仓位不再动了

                time.sleep(random.random() * random_sleep_multiplier_place_order)

                meth = publish_portfolio.get('use_portfolio_preprocess_function')
                meth = methods.get(meth)
                if meth is not None:
                    publish_portfolio = meth(publish_portfolio)

                now_portfolio = get_document_field('__portfolio__')
                targ_portfolio = transfer_to_targ_portfolio(publish_portfolio)

                change_position_to_target_position(now_portfolio=now_portfolio, targ_portfolio=targ_portfolio)

                set_document_field('__portfolio__', targ_portfolio)

                lock.release()

                ts_count_warning(ts_delta, count_delta, ts_max_delta)

        except:
            lock.release()
            logging.error(f'{traceback.format_exc()}')
            my_email(f'lineno: {lineno()}, MACHINE_NAME: {MACHINE_NAME}, CUSTOMER_MONGODB_ID: {CUSTOMER_MONGODB_ID}出现了报错问题', traceback.format_exc())


def get_able_to_trade():
    fields = ['__启动停止(散户用)__', '启动停止(我个人用)', '__启动停止(保证金用)__']
    able_to_trade_dict = get_document_fields(fields)
    able_to_trade_list = [int(el) for el in able_to_trade_dict.values()]
    able_to_trade = all(able_to_trade_list)
    return able_to_trade


def publish_portfolio_preprocess_1(publish_portfolio):
    customer_portfolio = get_document_field('__portfolio__')  # 只有季度的持仓, 没有次周的, 不会存在交割的问题
    logging.info(f'0 | 金本位币本位修改前, publish_position: {publish_portfolio["btc_quarter"]}, customer_position: {customer_portfolio["btc_quarter"]}')

    if __standard__ == 'gold':
        publish_portfolio["btc_quarter"][0] -= 1

    logging.info(f'1 | 金本位币本位修改后, publish_position: {publish_portfolio["btc_quarter"]}')

    customer_position = prev_customer_position = customer_portfolio['btc_quarter']  # 只有 portfolio_1 用这个 preprocess, 只有 btc_quarter 一个 field 有值
    publish_position, publish_position_change = publish_portfolio['btc_quarter']

    # 如果仓位不变
    if publish_position_change == 0:
        publish_portfolio['btc_quarter'] = [customer_position, 0]
        return publish_portfolio

    # 仓位有变化, 不需要注意穿过 0 点, 因为发布者已经做好了这个东西了
    customer_position += publish_position_change
    boundary = 0 if __standard__ == 'bitcoin' else -1

    if publish_position > boundary and publish_position_change > 0:  # 加多仓
        if customer_position > publish_position:
            logging.warning(f'publish_portfolio: {publish_portfolio}, '
                            f'customer_portfolio: {customer_portfolio}, customer_position: {customer_position}, '
                            f'publish_position: {publish_position}, 开多时, 客户的仓位大于了发布者的仓位, 有问题, '
                            f'但也可能是手动调整了仓位')
        customer_position = min(publish_position, customer_position)  # 不能超过 publish 的仓位, 虽然不可能超过

    elif publish_position < boundary and publish_position_change < 0:  # 加空仓
        if customer_position < publish_position:
            logging.warning(f'publish_portfolio: {publish_portfolio}, '
                            f'customer_portfolio: {customer_portfolio}, customer_position: {customer_position}, '
                            f'publish_position: {publish_position}, 开空时, 客户的仓位小于了发布者的仓位, 有问题, '
                            f'但也可能是手动调整了仓位')
        customer_position = max(publish_position, customer_position)  # publish_position_change 是负数

    elif publish_position >= boundary and publish_position_change < 0:  # 平多仓
        customer_position = max(boundary, customer_position)  # target 平完多之前不能开空
        if customer_position > publish_position:
            logging.warning(f'publish_portfolio: {publish_portfolio}, '
                            f'customer_portfolio: {customer_portfolio}, customer_position: {customer_position}, '
                            f'publish_position: {publish_position}, 平多时, 客户的仓位大于了发布者的仓位, 有问题, '
                            f'但也可能是手动调整了仓位')
        customer_position = min(publish_position, customer_position)

    elif publish_position <= boundary and publish_position_change > 0:  # 平空仓
        customer_position = min(boundary, customer_position)
        if customer_position < publish_position:
            logging.warning(f'publish_portfolio: {publish_portfolio}, '
                            f'customer_portfolio: {customer_portfolio}, customer_position: {customer_position}, '
                            f'publish_position: {publish_position}, 平空时, 客户的仓位小于了发布者的仓位, 有问题, '
                            f'但也可能是手动调整了仓位')
        customer_position = max(publish_position, customer_position)

    else:
        raise ValueError

    # 现在的 customer_position 已经是我需要的 customer_position 了, 可以直接用了
    publish_portfolio['btc_quarter'] = [float(customer_position), float(customer_position - prev_customer_position)]
    logging.info(f'经过 publish_portfolio_preprocess_1 后, publish_position: {publish_portfolio["btc_quarter"]}')

    return publish_portfolio


def set_initial_asset(last_run=[time.time()]):
    if __standard__ == 'bitcoin':
        spot_btc, futures_btc, have_position = api.get_btc_withdraw_amount()
        if have_position:
            logging.warning(f'无法重新设置初始化资金量, 有仓位, spot_btc: {spot_btc}, futures_btc: {futures_btc}, have_position: {have_position}')
            return

        # 如果交割合约的 btc 盈利 1.5 倍以上, 并且 spot 的数量 < 合同的用户资金量, 并且 1 天内只能转移一次
        if (futures_btc > get_document_field('__用户合同初始资金量(结算分红用)__') * (1 - get_document_field('__止损比例(不放入合约资金比例)__')) * 1.5) and (spot_btc < get_document_field('__用户合同初始资金量(结算分红用)__')) and (time.time() - last_run[0] > 1 * 24 * 3600):
            trans_to_spot_amount = futures_btc * 0.05
            api.transfer_btc(trans_to_spot_amount, True)
            spot_btc, futures_btc, have_position = api.get_btc_withdraw_amount()
            last_run[0] = time.time()

        initial_asset = futures_btc
        set_document_field('__initial_asset(used_to_calculate_zhang)__', initial_asset)
        logging.info(f'spot_btc: {spot_btc}, futures_btc: {futures_btc}, 重设了初始仓位, 初始仓位: {initial_asset}')

    elif __standard__ == 'gold':
        gold_standard_0_positoin_zhang, margin_balance, btc_price = api.get_gold_standard_0_position_zhang(return_all=True)  # > 0
        long_zhang, short_zhang = api.get_exchange_position()
        now_positoin_zhang = long_zhang - short_zhang
        if now_positoin_zhang < 0 and (abs(now_positoin_zhang - (-gold_standard_0_positoin_zhang)) < 1 or
                                       0.99 < (now_positoin_zhang / (-gold_standard_0_positoin_zhang)) < 1.01):  # 注意 now_positoin_zhang 和 gold_standard_0_positoin_zhang异号, 在只有空单的前提下, 小资金前者, 大资金用后者
            initial_asset_usd_amount = gold_standard_0_positoin_zhang * 100
            set_document_field('__initial_asset(used_to_calculate_zhang)__', initial_asset_usd_amount)
            logging.info(f'margin_balance: {margin_balance}, btc_price: {btc_price}, 重设了初始仓位, 初始仓位: {initial_asset_usd_amount}')

        else:
            logging.warning(f'已开单的张数和净资产的价值差距较大, 无法重设初始资金量, now_positoin_zhang: {now_positoin_zhang}, gold_standard_0_positoin_zhang: {gold_standard_0_positoin_zhang}')

    else:
        raise ValueError


def spot_buy_btc(usdt_amount, spot_usdt_should):
    while 1:
        able_to_trade = get_able_to_trade()
        if able_to_trade:
            break
        logging.warning(f'able_to_trade: {able_to_trade}')
        time.sleep(1)

    if usdt_amount < 0:
        logging.critical(f'usdt_amount: {usdt_amount}')
        my_email(f'lineno: {lineno()}, spot_buy_btc有问题, 低于 0 usdt', f'usdt_amount: {usdt_amount}')
        return

    logging.info(f'spot_buy_btc, usdt_amount: {usdt_amount}')

    order_keep_second = float(get_document_field('order_keep_second')) * 3

    i = 0
    while 1:
        i += 1
        now_spot_usdt = api.get_spot_usdt_withdraw_amount()
        residual_amount = now_spot_usdt - spot_usdt_should
        if residual_amount < 6:  # 最小下单 5 USDT
            break

        residual_amount = min(residual_amount, 30000)  # 现货一次买入, 不超过 3 万美元, 否则可能导致市场有波动
        ask_price = api.get_spot_btcusdt_price(return_bid_ask=True)['ask']
        btc_amount = '%.6f' % (residual_amount / ask_price)
        if float(btc_amount) == 0:
            break
        params = {
            'account-id': api.spot_account_id,
            'symbol': 'btcusdt',
            'type': 'buy-limit',
            'amount': btc_amount,
            'price': ask_price,
            'source': 'spot-api',
        }

        """
        {'status': 'error', 'err-code': 'order-value-min-error', 'err-msg': 'Order total cannot be lower than: `5`', 'data': None}
        """
        res = api.spot_place_order(params)

        if res['status'] == 'error' and res['err-code'] == 'order-value-min-error':
            api.spot_cancel_all_order()
            break

        time.sleep(order_keep_second)
        api.spot_cancel_all_order()

        if 100 <= i <= 300 and i % 50 == 0:
            my_email(f'现货买入, lineno: {lineno()}, 下单推土机下单了{i}次', '重大问题, 单子极有可能没有全部成交, 也可能开了超高倍的单子')
            logging.warning(f'警告 | 下单推土机下单第{i}次 | 超过 300 次不再发邮件提醒')


def move_asset():
    # 金本位: 获取现货的 usdt 数量, 不管 BTC 的数量, 也不管交割合约的 BTC 数量, 计算总的 usdt 的量, 看是不是和 register 的量是一致的, 把 usdt 的 register 的止损比例部分买成 BTC, 将止损比例的 BTC 全部提到交割合约, 并用逐仓开 100 倍杠杆, 并在合约市场卖出 1 倍杠杆.
    # 币本位: 获取现货和交割合约的 BTC 数量, 不管 usdt 的数量, 计算总的 BTC 的量, 看是不是和 register 的量是一致的, 将止损比例的 BTC 全部提到交割合约, 并用逐仓开 100 倍杠杆

    if not get_document_field('__asset_moved__'):
        if __standard__ == 'bitcoin':
            spot_btc_now, futures_btc_now, _ = api.get_btc_withdraw_amount()

            spot_btc_should = get_document_field('__用户合同初始资金量(结算分红用)__') * get_document_field('__止损比例(不放入合约资金比例)__')

            amount = spot_btc_now - spot_btc_should
            assert spot_btc_now + futures_btc_now > get_document_field('__用户合同初始资金量(结算分红用)__') * get_document_field('__止损比例(不放入合约资金比例)__'), '已达到止损比例'

            res = api.transfer_btc(abs(amount), to_spot=True if amount < 0 else False)
            logging.info(f'transfer_btc response: {res}, amount: {amount}')

            spot_btc_targ, futures_btc_targ = spot_btc_should, (spot_btc_now + futures_btc_now - spot_btc_should)
            spot_btc_now, futures_btc_now, _ = api.get_btc_withdraw_amount()
            assert get_document_field('__止损比例(不放入合约资金比例)__') == 0 or 0.99 < (spot_btc_targ / spot_btc_now) < 1.01
            assert 0.99 < (futures_btc_targ / futures_btc_now) < 1.01

            set_document_field('__asset_moved__', True)

            set_initial_asset()

        elif __standard__ == 'gold':
            _, futures_btc_now, _ = api.get_btc_withdraw_amount()
            assert futures_btc_now <= 0.0001

            spot_usdt = api.get_spot_usdt_withdraw_amount()
            spot_usdt_should = get_document_field('__用户合同初始资金量(结算分红用)__') * get_document_field('__止损比例(不放入合约资金比例)__')
            usdt_amount_buy_btc = spot_usdt - spot_usdt_should
            assert usdt_amount_buy_btc > 0, '已达到止损比例'

            # 可以用 2 BTC 的量, 用对手价买入 BTC
            spot_buy_btc(usdt_amount_buy_btc, spot_usdt_should)

            spot_btc_now, _, _ = api.get_btc_withdraw_amount()

            res = api.transfer_btc(spot_btc_now, to_spot=False)
            logging.info(f'transfer_btc response: {res}, spot_btc_now: {spot_btc_now}')

            now_portfolio = {
                'spot': 0,
                'btc_this_week': 0,
                'btc_next_week': 0,
                'btc_quarter': 0,
                'btc_bi_quarter': 0,
                'btc_swap': 0,
                'usdt_swap': 0,
            }

            targ_portfolio = {
                'spot': 0,
                'btc_this_week': 0,
                'btc_next_week': 0,
                'btc_quarter': -1,
                'btc_bi_quarter': 0,
                'btc_swap': 0,
                'usdt_swap': 0,
            }
            change_position_to_target_position(now_portfolio=now_portfolio, targ_portfolio=targ_portfolio)

            set_document_field('__portfolio__', targ_portfolio)

            set_document_field('__asset_moved__', True)

        else:
            raise ValueError


def open_position_trade(standard_coin_amount, direction, offset):
    logging.info(f'standard_coin_amount: {standard_coin_amount}, direction: {direction}, offset: {offset}')
    """
    开多：买入开多(direction用buy、offset用open)
    开空：卖出开空(direction用sell、offset用open)
    """

    assert standard_coin_amount >= 0, 'standard_coin_amount 必须是正数'
    assert offset == 'open', 'offset 必须是 open'

    if direction == 'buy':
        sign = 1
    elif direction == 'sell':
        sign = -1
    else:
        raise ValueError

    price = api.get_quarter_price()

    if __standard__ == 'bitcoin':
        bitcoin = standard_coin_amount
        usd_amount = bitcoin * price
    elif __standard__ == 'gold':
        usd_amount = standard_coin_amount
    else:
        raise ValueError

    zhang = usd_amount / ZHANG_UNIT
    account_now_zhang = get_document_field('__account_should_ZHANG__')
    account_should_ZHANG = account_now_zhang + zhang * sign

    set_document_field('__account_should_ZHANG__', account_should_ZHANG)

    trade_till_done()


def close_position_trade(close_percent, direction, offset):
    # 注意计算张数的时候, 金本位 要减去维持 0 仓位的张数
    # 平多的时候要注意, 算上维持 0 仓位要开空的张数
    # now_position < targ_position <= boundary
    # boundary <= targ_position < now_position
    logging.info(f'direction: {direction}, offset: {offset}, close_percent: {close_percent}')

    close_percent = abs(close_percent)
    """
    平多：卖出平多(direction用sell、offset用close)
    平空：买入平空(direction用buy、offset用close)
    """

    assert offset == 'close', 'offset 必须是 close'

    if __standard__ == 'bitcoin':
        account_now_zhang = get_document_field('__account_should_ZHANG__')
        account_should_zhang = account_now_zhang * (1 - close_percent)
    elif __standard__ == 'gold':
        account_now_zhang = get_document_field('__account_should_ZHANG__')  # 大于 0 或者小于 0
        gold_standard_0_positoin_zhang = api.get_gold_standard_0_position_zhang()  # > 0
        # account_now_zhang > -1 的仓位 加上 100 张 0_positoin_zhang, account_now_zhang < -1 的仓位, 负值加上 100 张
        # 0_positoin_zhang 是 100 张做空, close_percent=0.2
        # 现在 50 张, 实际相当于 150 张做多, 平掉 0.2, 150 * (1 - 0.2) = 120, should_zhang = 120 - 100 = 20 张.
        # 现在-50 张, 实际相当于 50 张做多, 平掉 0.2, 50 * (1 - 0.2) = 40 张, should_zhang = 40-100 = -60 张.
        # 现在-100 张, 相当于 account_now_zhang = 0 张, 平掉 0.2, 还是 0 张,  should_zhang = 0 -100 = -100 张.
        # 现在-150 张, 相当于 50 张做空(account_now_zhang = -50), 平掉 0.2, -50 * 0.8 = -40, -40 - 100 = -140 张.
        account_zhang_plus = account_now_zhang + gold_standard_0_positoin_zhang
        account_should_zhang_plus = account_zhang_plus * (1 - close_percent)
        account_should_zhang = account_should_zhang_plus - gold_standard_0_positoin_zhang

    else:
        raise ValueError

    set_document_field('__account_should_ZHANG__', account_should_zhang)
    trade_till_done()


def change_position_to_target_position(now_portfolio, targ_portfolio):
    def get_close_percent(targ_position, now_position):
        if __standard__ == 'bitcoin':
            return abs((targ_position - now_position) / now_position)
        elif __standard__ == 'gold':
            return abs(((targ_position + 1) - (now_position + 1)) / (now_position + 1))
        else:
            raise ValueError

    now_position = float(now_portfolio['btc_quarter'])
    targ_position = float(targ_portfolio['btc_quarter'])

    logging.info(f'now_position: {now_position}, target_position: {targ_position}')

    if now_position == targ_position:
        return None

    initial_asset = get_document_field('__initial_asset(used_to_calculate_zhang)__')

    """
    开多：买入开多(direction用buy、offset用open)
    平多：卖出平多(direction用sell、offset用close)
    开空：卖出开空(direction用sell、offset用open)
    平空：买入平空(direction用buy、offset用close)
    """

    boundary = -1 if __standard__ == 'gold' else 0

    # 如果是币本位, 不会经过0, 金本位不会经过 -1
    # 买入BTC, 看涨
    if targ_position > now_position:
        # 开BTC的多仓
        if boundary <= now_position < targ_position:
            if now_position == boundary:
                set_initial_asset()
            standard_coin_amount = (targ_position - now_position) * initial_asset
            open_position_trade(standard_coin_amount, 'buy', 'open')

        # 平BTC的空仓
        elif now_position < targ_position <= boundary:
            close_percent = get_close_percent(targ_position, now_position)
            close_position_trade(close_percent, 'buy', 'close')
            if targ_position == boundary:
                set_initial_asset()

        # 经过零点, 先平BTC的空仓, 再开BTC的多仓
        elif now_position < boundary < targ_position:
            raise ValueError(lineno())

        else:
            raise ValueError(lineno())

    # 卖出BTC, 看跌
    elif targ_position < now_position:
        # 开BTC的空仓
        if targ_position < now_position <= boundary:
            if now_position == boundary:
                set_initial_asset()
            standard_coin_amount = -1 * (targ_position - now_position) * initial_asset
            open_position_trade(standard_coin_amount, 'sell' , 'open')

        # 平BTC的多仓
        elif boundary <= targ_position < now_position:
            close_percent = get_close_percent(targ_position, now_position)
            close_position_trade(close_percent, 'sell' , 'close')
            if targ_position == boundary:
                set_initial_asset()

        # 经过零点, 先平BTC的多仓, 再开BTC的空仓
        elif targ_position < boundary < now_position:
            raise ValueError(lineno())

        else:
            raise ValueError(lineno())

    else:
        raise ValueError(lineno())


def trade_till_done():
    account_should_zhang = get_document_field('__account_should_ZHANG__')
    long_zhang, short_zhang = api.get_exchange_position()  # 币本位的才能用这个, 如果是金本位的, 会先卖空 1 倍, 这个就出问题了
    assert long_zhang * short_zhang == 0
    account_now_zhang = long_zhang - short_zhang
    assert type(account_now_zhang) == int

    if account_should_zhang == account_now_zhang:
        return

    """
    开多：买入开多(direction用buy、offset用open)
    平多：卖出平多(direction用sell、offset用close)
    开空：卖出开空(direction用sell、offset用open)
    平空：买入平空(direction用buy、offset用close)
    """

    if account_now_zhang == 0:  # 开仓, 多 / 空
        offset = 'open'
        if account_should_zhang > 0:  # 开多
            direction = 'buy'
        elif account_should_zhang < 0:  # 开空
            direction = 'sell'
        else:
            raise ValueError

        zhang = abs(round(account_should_zhang))
        place_order(zhang, direction, offset)

    elif account_now_zhang < 0:
        if account_should_zhang > 0:  # 平空 + 开多
            # 平空
            zhang = abs(account_now_zhang)
            direction = 'buy'
            offset = 'close'
            place_order(zhang, direction, offset)

            # 开多
            zhang = abs(round(account_should_zhang))
            direction = 'buy'
            offset = 'open'
            place_order(zhang, direction, offset)

        elif account_should_zhang < 0:
            if account_now_zhang < account_should_zhang < 0:  # 平空
                zhang = abs(round(account_should_zhang - account_now_zhang))
                direction = 'buy'
                offset = 'close'
                place_order(zhang, direction, offset)

            elif account_should_zhang < account_now_zhang < 0:  # 开空
                zhang = abs(round(account_should_zhang - account_now_zhang))
                direction = 'sell'
                offset = 'open'
                place_order(zhang, direction, offset)

            else:
                raise ValueError

        elif account_should_zhang == 0:  # 平空
            zhang = abs(round(account_now_zhang))
            direction = 'buy'
            offset = 'close'
            place_order(zhang, direction, offset)

        else:
            raise ValueError

    elif account_now_zhang > 0:
        if account_should_zhang < 0:  # 平多 开空
            # 平多
            zhang = abs(round(account_now_zhang))
            direction = 'sell'
            offset = 'close'
            place_order(zhang, direction, offset)

            # 开空
            zhang = abs(round(account_should_zhang))
            direction = 'sell'
            offset = 'open'
            place_order(zhang, direction, offset)

        elif account_should_zhang > 0:
            if account_now_zhang > account_should_zhang > 0:  # 平多
                zhang = abs(round(account_should_zhang - account_now_zhang))
                direction = 'sell'
                offset = 'close'
                place_order(zhang, direction, offset)

            elif account_should_zhang > account_now_zhang > 0:  # 开多
                zhang = abs(round(account_should_zhang - account_now_zhang))
                direction = 'buy'
                offset = 'open'
                place_order(zhang, direction, offset)

            else:
                raise ValueError

        elif account_should_zhang == 0:  # 平多
            zhang = abs(round(account_now_zhang))
            direction = 'sell'
            offset = 'close'
            place_order(zhang, direction, offset)

        else:
            raise ValueError

    else:
        raise ValueError


def place_order(zhang, direction, offset):
    """
    开多：买入开多(direction用buy、offset用open)
    平多：卖出平多(direction用sell、offset用close)
    开空：卖出开空(direction用sell、offset用open)
    平空：买入平空(direction用buy、offset用close)
    """

    def distribute_zhang(zhang, max_zhang, detail=None):
        """detail = {
            'this_week': {'buy': 0, 'sell': 1200},
            'next_week': {'buy': 0, 'sell': 120},
            'quarter': {'buy': 0, 'sell': 20},
            'next_quarter': {'buy': 0, 'sell': 0}
        }"""
        if detail is None:
            zhang_list = []
            while zhang > 0:
                if zhang <= max_zhang:
                    zhang_list.append(zhang)
                    zhang = 0
                else:
                    zhang_list.append(max_zhang)
                    zhang -= max_zhang
            return zhang_list
        else:
            keys = ['this_week', 'next_week', 'quarter', 'next_quarter']
            zhang_and_contract_type_list = []
            for key in keys:
                amount = detail[key]['buy' if direction == 'sell' else 'sell']
                while zhang > 0 and amount > 0:
                    if zhang <= min(amount, max_zhang):
                        zhang_and_contract_type_list.append([zhang, key])
                        zhang = 0
                        amount -= zhang
                    else:
                        zhang_and_contract_type_list.append([min(amount, max_zhang), key])
                        zhang -= min(amount, max_zhang)
                        amount -= min(amount, max_zhang)
            return zhang_and_contract_type_list

    assert zhang % 1 == 0
    zhang = int(zhang)

    while 1:
        able_to_trade = get_able_to_trade()
        if able_to_trade:
            break
        logging.warning(f'able_to_trade: {able_to_trade}')
        time.sleep(1)

    if zhang < 0:
        logging.critical(f'zhang: {zhang}, direction: {direction} , offset: {offset}')
        my_email(f'lineno: {lineno()}, 下单张数有问题, 低于 0 张', f'zhang: {zhang}, direction: {direction} , offset: {offset}')
        return
    elif zhang == 0:
        return

    logging.info(f'trade_till_done, 准备决定期货下单标的zhang: {zhang}, direction: {direction}, offset: {offset}')

    place_order_dict_list = []
    max_zhang = get_document_field('max_zhang')

    if offset == 'open':
        zhang_list = distribute_zhang(zhang, max_zhang)
        for zhang in zhang_list:
            place_order_dict_list.append({
                'zhang': zhang, 'direction': direction, 'offset': offset, 'contract_type': 'quarter'
            })

    elif offset == 'close':
        _, _, detail = api.get_exchange_position(return_detail=True)
        zhang_and_contract_type_list = distribute_zhang(zhang, max_zhang, detail)
        for (zhang, contract_type) in zhang_and_contract_type_list:
            place_order_dict_list.append({
                'zhang': zhang, 'direction': direction, 'offset': offset, 'contract_type': contract_type
            })

    logging.info(f'trade_till_done, 已决定期货下单标的, place_order_dict_list: {place_order_dict_list}')

    T = 1000
    i = 0
    order_keep_second = get_document_field('order_keep_second')
    for place_order_dict in place_order_dict_list:
        for i in range(T):
            # 下单
            res = api.place_order(**place_order_dict)
            return_ts = time.time()

            try:
                assert res['status'] == 'ok'
                order_id = res['data']['order_id']
            except:
                api.cancel_all_order()
                logging.critical(f'下单返回的信息有问题, res: {res}')
                return None  # 下次可以继续开单, should_zhang 已经存下了

            time.sleep(order_keep_second - min(order_keep_second, (time.time() - return_ts)))

            # 取消所有订单
            api.cancel_all_order()

            # 获取订单信息
            residual, volume , trade_volume = api.get_order_residual(order_id)
            logging.info(f'trade_till_done, 已开单, i:{i}, zhang: {volume}, '
                         f'filled: {trade_volume}, residual: {residual}, direction: {place_order_dict["direction"]}, '
                         f'offset: {place_order_dict["offset"]} , contract_type: {place_order_dict["contract_type"]}, '
                         f'order_id: {order_id}')

            assert int(volume) == int(place_order_dict['zhang']), '张数不等于开单的数量, 这里有问题'
            place_order_dict['zhang'] = residual

            if place_order_dict['zhang'] == 0:
                break
            else:
                if 10 <= i <= 30 and i % 10 == 0:
                    logging.warning(f'警告 | 下单推土机下单第{i}次 | 超过 30 次不再发邮件提醒')

        if i == T - 1:
            logging.critical(f'下单推土机下单了{i}次, 然后退出了, 单子极有可能没有全部成交, 也可能开了超高倍的单子, place_order_dict: {place_order_dict}')
            my_email(f'lineno: {lineno()}, 下单推土机下单了{i}次, 然后退出了', f'重大问题, 单子极有可能没有全部成交, 也可能开了超高倍的单子, place_order_dict: {place_order_dict}')


def check_initial_asset_with_customer_contract_amount():
    if not get_document_field('__asset_moved__'):

        long_zhang, short_zhang = api.get_exchange_position()
        assert long_zhang == short_zhang == 0

        if __standard__ == 'bitcoin':
            spot_btc_now, futures_btc_now, _ = api.get_btc_withdraw_amount()
            btc_in_account = spot_btc_now + futures_btc_now

            customer_contract_amount = float(get_document_field('__用户合同初始资金量(结算分红用)__'))
            if 0.999 < (btc_in_account / customer_contract_amount) < 1.01:
                logging.info(f'第一次开始量化, 检查BTC数量结果: '
                             f'spot_btc_now: {spot_btc_now} , futures_btc_now: {futures_btc_now}, '
                             f'btc_in_account: {btc_in_account} , customer_contract_amount: '
                             f'{customer_contract_amount}, BTC查到的数量和合同的数量几乎一样, 开始量化')
            else:
                logging.error(f'第一次开始量化, 检查BTC数量结果: '
                              f'spot_btc_now: {spot_btc_now} , futures_btc_now: {futures_btc_now}, '
                              f'btc_in_account: {btc_in_account} , customer_contract_amount: '
                              f'{customer_contract_amount}, BTC查到的数量和合同的数量差距较大, 检查原因')
                my_email(f'lineno: {lineno()}, btc查到的数量和合同的数量差距较大, 检查原因, 已关闭量化', f''
                                                            f'第一次开始量化, 检查BTC数量结果: spot_btc_now: '
                                                            f'{spot_btc_now} , futures_btc_now: {futures_btc_now}, '
                                                            f'btc_in_account: {btc_in_account} , '
                                                            f'customer_contract_amount: {customer_contract_amount}, '
                                                            f'BTC查到的数量和合同的数量差距较大, 检查原因')
                raise ValueError

        elif __standard__ == 'gold':
            spot_usdt = api.get_spot_usdt_withdraw_amount()
            customer_contract_amount = float(get_document_field('__用户合同初始资金量(结算分红用)__'))

            if 0.999 < spot_usdt / customer_contract_amount < 1.01:
                logging.info(f'第一次开始量化, 检查BTC数量结果: '
                             f'spot_usdt: {spot_usdt} , customer_contract_amount: {customer_contract_amount}, '
                             f'BTC查到的数量和合同的数量几乎一样, 开始量化')
            else:
                logging.error(f'第一次开始量化, 检查BTC数量结果: '
                              f'spot_usdt: {spot_usdt} , customer_contract_amount: {customer_contract_amount}, '
                              f'BTC查到的数量和合同的数量差距较大, 检查原因')
                my_email(f'lineno: {lineno()}, btc查到的数量和合同的数量差距较大, 检查原因, 已关闭量化',
                             f'第一次开始量化, 检查BTC数量结果: spot_usdt: {spot_usdt}, '
                             f'customer_contract_amount: {customer_contract_amount}, '
                             f'BTC查到的数量和合同的数量差距较大, 检查原因')
                raise ValueError

        else:
            raise ValueError


def trans_next_week_to_quarter():
    """
    detail = {
        'this_week': {'buy': 0, 'sell': 0},
        'next_week': {'buy': 0, 'sell': 0},
        'quarter': {'buy': 0, 'sell': 0},
        'next_quarter': {'buy': 0, 'sell': 0}
    }
    """

    def need_to_transfer(detail):
        for field in ['this_week', 'next_week']:
            if list(detail[field].values()) != [0, 0]:
                return True
        return False

    while 1:
        long_zhang, short_zhang, detail = api.get_exchange_position(return_detail=True)
        if not need_to_transfer(detail):
            time.sleep(60)
            continue

        # 需要做移仓
        lock.acquire()

        try:
            long_zhang, short_zhang, detail = api.get_exchange_position(return_detail=True)
            if not need_to_transfer(detail):
                continue

            logging.info(f'需要移仓, long_zhang: {long_zhang}, short_zhang: {short_zhang}, detail: {detail}')

            assert long_zhang * short_zhang == 0, f'long_zhang: {long_zhang}, short_zhang: {short_zhang}'

            transfer_list = []
            buy_sell_amount = [
                detail['this_week']['buy'] + detail['next_week']['buy'],
                detail['this_week']['sell'] + detail['next_week']['sell'],
            ]
            assert not (buy_sell_amount[0] == buy_sell_amount[1] == 0)
            assert buy_sell_amount[0] * buy_sell_amount[1] == 0

            """place_order(zhang, direction, offset)"""
            """
            开多：买入开多(direction用buy、offset用open)
            平多：卖出平多(direction用sell、offset用close)
            开空：卖出开空(direction用sell、offset用open)
            平空：买入平空(direction用buy、offset用close)
            """

            if buy_sell_amount[0] == 0:  # 有空单, 平空, 在开空
                transfer_list.append({'zhang': buy_sell_amount[1], 'direction': 'buy', 'offset': 'close'})
                transfer_list.append({'zhang': buy_sell_amount[1], 'direction': 'sell', 'offset': 'open'})
            elif buy_sell_amount[1] == 0:  # 有多单, 平多, 再开多
                transfer_list.append({'zhang': buy_sell_amount[0], 'direction': 'sell', 'offset': 'close'})
                transfer_list.append({'zhang': buy_sell_amount[0], 'direction': 'buy', 'offset': 'open'})

            random.shuffle(transfer_list)

            logging.info(f'transfer_list: {transfer_list}')

            for kwargs in transfer_list:
                place_order(**kwargs)

        except:
            logging.error(f'ERROR: {traceback.format_exc()}')

        lock.release()


if __name__ == '__main__':
    logging.info('开始')
    # 订阅 redis 的 portfolio
    ps.subscribe(get_document_field('__REDIS_PUBLISH_ID__'))

    __standard__ = get_document_field('__standard__')
    assert __standard__ in {'gold', 'bitcoin'}
    ZHANG_UNIT = 100 if __standard__ == 'bitcoin' else 100  # 这里都是 btc/usd 的交割合约, 不管金本位还是币本位, 都在币本位合约

    api = HuobiAPI(ACCESS_KEY, SECRET_KEY)
    is_sub_account = api.check_sub_account()
    if not is_sub_account:
        logging.error(f'不是子账户')
    assert is_sub_account

    # 检查资金量和合同资金量是否一致只会在第一次启动时检查
    if not get_document_field('__asset_moved__'):
        """https://huobiapi.github.io/docs/spot/v1/cn/#e227a2a3e8
        2020/12/02 - 15:13:33 | 1335 | CRITICAL | place_order | 5fc73e721ba2545a37520870 | ali_portfolio | 下单返回的信息有问题, res: {'status': 'error', 'err_code': 1233, 'err_msg': 'High leverage is not enabled (Please sign in the APP or web with your main account to agree to the High-Leverage Agreement)', 'ts': 1606893213213}
        """
        """
        检查合约是不是没有开单"""
        logging.info(f'未进行过仓位变动, 是第一次运行, 进行资金量检测和资金迁移至合约账户')
        check_initial_asset_with_customer_contract_amount()
        move_asset()
        logging.info(f'已通过检查, 开始量化')
    else:
        logging.info(f'进行过仓位变动, 不是第一次运行, 不进行资金量检测和资金迁移至合约账户')

    methods = {
        'publish_portfolio_preprocess_1': publish_portfolio_preprocess_1,
    }
    lock = Lock()

    executor = ThreadPoolExecutor(4)
    # 接下来要做好接收的一个 redis 的 subscrib, 防止漏了信息, 虽然漏了几条问题不大
    executor.submit(customer)
    executor.submit(manual_change_portfolio)
    executor.submit(trans_next_week_to_quarter)
    executor.shutdown()
    logging.error(f'量化停止了')
    my_email(f'lineno: {lineno()}, 量化停止了', f'量化停止了')
