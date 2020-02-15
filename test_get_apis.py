# -*- coding: utf-8 -*-
# @Author: MirrorAi
# @Date:   2020/2/14 20:32

import requests
import json
import pytest
from api_information import api_info, main_url, tokens


class HttpRequests(object):

    def __init__(self):
        # 初始化会话
        self.session = requests.Session()

    def send_request(self, method, url, params=None, json=None, headers=None, **kwargs):
        method = method.upper()

        if method == 'GET':
            response = self.session.get(url, params=params, headers=headers, **kwargs)
        elif method == 'POST':
            response = self.session.post(url, json=json, params=params, headers=headers, **kwargs)
        elif method == 'PUT':
            response = self.session.put(url, json=json, headers=headers, **kwargs)
        elif method == 'DELETE':
            response = self.session.delete(url, json=json, headers=headers, **kwargs)
        else:
            raise ValueError('request method: %s is not support' % method)

        return response

    def close_session(self):
        # 关闭会话
        self.session.close()


def send_get_request(method, url, params, headers):
    test_session = HttpRequests()
    response = test_session.send_request(method, url, params=params, headers=headers)
    test_session.close_session()
    return response


def test_get_user_profile():
    '''
        获取用户信息
    '''
    api = api_info[2]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_protocol_check_result():
    '''
        获取用户协议同意情况
    '''
    api = api_info[4]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_status_number():
    '''
        获取用户买卖数量
    '''
    api = api_info[5]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_newuser_check_result():
    '''
        获取用户是否新用户
    '''
    api = api_info[6]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_epcoupon_list():
    '''
        获取用户优惠券列表
    '''
    api = api_info[8]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_favorite_notice_arrival_list():
    '''
        获取用户到货提醒列表
    '''
    api = api_info[9]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookfee_log():
    '''
        获取用户书费明细
    '''
    api = api_info[11]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_money_log():
    '''
        获取用户余额明细
    '''
    api = api_info[11]
    api['api_headers']['Authorization'] = tokens['token']
    api['api_params']['currency'] = 2
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_address_list():
    '''
        获取用户地址列表
    '''
    api = api_info[12]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_system_banner():
    '''
        获取弹窗配置
    '''
    api = api_info[15]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_visitor_profile():
    '''
        获取未登录状态用户信息（游客状态）
    '''
    api = api_info[16]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_all_usual_book_list():
    '''
        获取全部普通书单
    '''
    api = api_info[17]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_all_activity_book_list():
    '''
        获取全部活动书单
    '''
    api = api_info[17]
    api['api_params']['type'] = 1
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_recommend_book_group():
    '''
        获取推荐分类
    '''
    api = api_info[18]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_all_book_group():
    '''
        获取全部分类
    '''
    api = api_info[19]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_recommend_book():
    '''
        获取首页推荐书籍
    '''
    api = api_info[20]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_recommend_book_list():
    '''
        获取首页推荐书单
    '''
    api = api_info[21]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_books_of_book_group():
    '''
        获取分类下书籍列表
    '''
    api = api_info[22]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_configuration_of_book_list():
    '''
        获取推书单配置信息
    '''
    api = api_info[23]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_putaway_book():
    '''
        获取最新上架书籍
    '''
    api = api_info[24]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_book_detail():
    '''
        获取图书详情
    '''
    api = api_info[25]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


@pytest.mark.g
def test_get_books_of_book_list():
    '''
        获取书单下书籍列表
    '''
    api = api_info[26]
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_profilelite():
    '''
        获取个人书架专用用户信息
    '''
    api = api_info[27]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_favorite():
    '''
        获取个人书架-我的藏书列表
    '''
    api = api_info[28]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_sold():
    '''
        获取个人书架-已卖出列表
    '''
    api = api_info[29]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_like():
    '''
        获取个人书架-想读列表
    '''
    api = api_info[30]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_followers_list():
    '''
        获取个人书架-关注我的用户列表
    '''
    api = api_info[31]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_follows_person_list():
    '''
        获取个人书架-我关注的用户列表
    '''
    api = api_info[31]
    api['api_headers']['Authorization'] = tokens['token']
    api['api_params']['as_follower'] = 1
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_bookshelf_book_hunt_user_list():
    '''
        获取个人书架-向我求购的用户列表
    '''
    api = api_info[32]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_favorite_detail():
    '''
        获取个人书架-我的藏书中某本书的详细信息
    '''
    api = api_info[33]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_favorite_hunters():
    '''
        获取个人书架-我的藏书中某本书的求购者列表
    '''
    api = api_info[34]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_bookshelf_spu_id():
    '''
        个人书架页 ，使用isbn查询spu
    '''
    api = api_info[35]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_user_bookshelf_favorite_collector():
    '''
        获取某本书在个人书架-我的藏书列表中的记录（除本人，拥有这本书的人列表）
    '''
    api = api_info[37]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_recycle_order_list():
    '''
        获取回收订单列表
    '''
    api = api_info[41]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_recycle_order_detail():
    '''
        获取回收订单详细信息
    '''
    api = api_info[42]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_recycle_order_pickup():
    '''
        获取创建回收订单时，当前可选预约取件时间
    '''
    api = api_info[45]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_recycle_cart_book_list():
    '''
        获取图书回收车中商品列表
    '''
    api = api_info[46]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_recycle_cart_book_spu_id():
    '''
        回收部分，通过isbn查询spu
    '''
    api = api_info[47]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_sell_order_list():
    '''
        获取销售订单列表
    '''
    api = api_info[52]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_sell_cart_goods_list():
    '''
        获取购物车中书籍列表
    '''
    api = api_info[55]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_sell_reserve_book_list():
    '''
        获取预订图书列表
    '''
    api = api_info[56]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_sell_order_detail():
    '''
        获取销售订单详情
    '''
    api = api_info[65]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_book_recommend_has_stock_list():
    '''
        获取图书详情页-相关推荐-有货的书籍列表
    '''
    api = api_info[66]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_book_recommend_all_list():
    '''
        获取图书详情页-相关推荐-全部书籍列表
    '''
    api = api_info[67]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_book_recommend_search_by_tag():
    '''
        获取图书详情页-相关推荐-标签搜索结果
    '''
    api = api_info[68]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_book_search_by_tag():
    '''
        获取按标签搜索结果列表
    '''
    api = api_info[69]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_book_search_no_stock():
    '''
        获取搜索结果中无库存图书
    '''
    api = api_info[70]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_book_search_has_stock():
    '''
        获取搜索结果中有库存图书
    '''
    api = api_info[71]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_task_list():
    '''
        获取运营任务列表
    '''
    api = api_info[74]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_task_reward_amount():
    '''
        获取任务完成奖励合计
    '''
    api = api_info[75]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0


def test_get_task_bookfee_history():
    '''
        获取任务完成奖励书费明细
    '''
    api = api_info[76]
    api['api_headers']['Authorization'] = tokens['token']
    r = send_get_request(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_headers'])
    r_json = json.loads(r.text)
    assert r.status_code == 200
    assert r_json['code'] == 0
