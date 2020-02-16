# -*- coding: utf-8 -*-
# @Author: MirrorAi
# @Date:   2020/2/16 17:21

import pytest
import json
from api_information import api_info, tokens, main_url
from test_get_apis import HttpRequests
from tools import get_random_recipients


address_total = 0
address_recipients = get_random_recipients()
address_id = 0


def send_requests(method, url, params=None, json=None, headers=None, **kwargs):
    test_session = HttpRequests()
    response = test_session.send_request(method, url, params=params, json=json, headers=headers, **kwargs)
    test_session.close_session()
    return response


class TestAddAddress:
    '''
    测试新增地址功能
    新增成功后，地址列表长度+1，地址列表最后一项为新增地址
    '''

    @pytest.mark.run(order=1)
    def test_get_address_list(self):
        '''
        获取用户地址列表
        '''
        global address_total
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        r_json = json.loads(r.text)
        address_total = r_json['data']['total']
        # print(self.address_total)
        assert r.status_code == 200
        assert r_json['code'] == 0

    @pytest.mark.run(order=2)
    def test_add_address(self):
        '''
        添加地址
        '''
        api = api_info[13]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['recipients'] = address_recipients
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        r_json = json.loads(r.text)
        assert r.status_code == 200
        assert r_json['code'] == 0

    @pytest.mark.run(order=3)
    def test_get_address_new_list(self):
        '''
        获取用户地址列表
        '''
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        r_json = json.loads(r.text)
        assert r.status_code == 200
        assert r_json['code'] == 0
        assert r_json['data']['total'] == address_total+1
        assert r_json['data']['list'][-1]['recipients'] == address_recipients


class TestModifyAddress:
    '''
    测试修改地址功能
    修改成功后，原地址相应信息发生改变；地址列表长度不变
    '''

    @pytest.mark.run(order=1)
    def test_get_address_list(self):
        '''
        获取用户地址列表
        '''
        global address_id
        global address_total
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        r_json = json.loads(r.text)
        address_id = r_json['data']['list'][1]['id']
        address_total = r_json['data']['total']
        assert r.status_code == 200
        assert r_json['code'] == 0

    @pytest.mark.run(order=2)
    def test_modify_address(self):
        '''
        修改地址
        '''
        api = api_info[14]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['recipients'] = address_recipients
        api['api_body']['id'] = address_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        r_json = json.loads(r.text)
        assert r.status_code == 200
        assert r_json['code'] == 0

    @pytest.mark.run(order=3)
    def test_get_modify_result(self):
        '''
        验证修改后地址是否与提交内容一致
        '''
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        r_json = json.loads(r.text)
        for address in r_json['data']['list']:
            if address['id'] == address_id:
                assert address['recipients'] == address_recipients
        assert r.status_code == 200
        assert r_json['code'] == 0
        assert r_json['data']['total'] == address_total
