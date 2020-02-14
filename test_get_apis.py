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


def assert_GET_APIs(method, url, params=None, headers=None):
    test_session = HttpRequests()
    response = test_session.send_request(method, url, params, headers)
    test_session.close_session()
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['code'] == 0


def test_GET_APIs():

    test_apis = []

    for i in range(api_info.__len__()):
        if api_info[i+1]['api_method'] == 'GET':
            api_info[i+1]['api_headers']['Authorization'] = tokens['token']
            test_apis.append(api_info[i+1])

    for api in test_apis:
        assert_GET_APIs(api['api_method'], main_url+api['api_url'], api['api_params'], api['api_headers'])


# if __name__ == '__main__':
#     pytest.main('test_get_apis.py')
