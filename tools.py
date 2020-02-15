# -*- coding: utf-8 -*-
# @Author: MirrorAi
# @Date:   2020/2/12 22:21

# import requests
#
#
# class HttpRequests(object):
#
#     def __init__(self):
#         # 初始化会话
#         self.session = requests.Session()
#
#     def send_request(self, method, url, params=None, json=None, headers=None, **kwargs):
#         method = method.upper()
#
#         if method == 'GET':
#             response = self.session.get(url, params=params, headers=headers, **kwargs)
#         elif method == 'POST':
#             response = self.session.post(url, json=json, params=params, headers=headers, **kwargs)
#         elif method == 'PUT':
#             response = self.session.put(url, json=json, headers=headers, **kwargs)
#         elif method == 'DELETE':
#             response = self.session.delete(url, json=json, headers=headers, **kwargs)
#         else:
#             raise ValueError('request method: %s is not support' % method)
#
#         return response
#
#     def close_session(self):
#         # 关闭会话
#         self.session.close()


import openpyxl
import json
from api_information import api_info, main_url, tokens

# d = {}
#
#
# def func(x):
#     # 确保headers、params、body值为空时，类型保持一致（dict）
#     if x is None:
#         return {}
#     else:
#         return json.loads(x)
#
#
# def make_dict(api_group, api_name, api_method, api_url, api_headers, api_params, api_body):
#     # 使用特定字段组成字典
#     d2 = {}
#     d2['api_group'] = api_group
#     d2['api_name'] = api_name
#     d2['api_method'] = api_method
#     d2['api_url'] = api_url
#     d2['api_headers'] = func(api_headers)
#     d2['api_params'] = func(api_params)
#     d2['api_body'] = func(api_body)
#     return d2
#
#
# # 从excel中获取接口信息，最后组成如下字典：
# # apis = {
# #     case_id:{'api_group':api_group, 'api_name':api_name, ...},
# # }
# with openpyxl.load_workbook('manyoujing_APIs.xlsx') as wb:
#     sh = wb['Sheet1']  # 选取表单
#     sh_contain = list(sh.rows)
#
#     for cases in list(sh.rows)[1:]:
#         case_id = cases[0].value
#         api_group = cases[1].value
#         api_name = cases[2].value
#         api_method = cases[3].value.upper()
#         api_url = cases[4].value
#         api_headers = cases[5].value
#         api_params = cases[6].value
#         api_body = cases[7].value
#         d[case_id] = make_dict(api_group, api_name, api_method, api_url, api_headers, api_params, api_body)
#
# for i in range(d.__len__()):
#     print(d[i+1])


# 获取get请求
def get_test_apis():
    test_apis = []
    for i in range(api_info.__len__()):
        if api_info[i + 1]['api_method'] == 'GET':
            api_info[i + 1]['api_headers']['Authorization'] = tokens['token']
            test_apis.append(api_info[i + 1])
    return test_apis


