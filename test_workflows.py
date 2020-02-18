# -*- coding: utf-8 -*-
# @Author: MirrorAi
# @Date:   2020/2/16 17:21

import pytest
import json
import random
from api_information import api_info, tokens, main_url
from test_get_apis import HttpRequests
from tools import get_random_recipients


address_total = 0
address_recipients = get_random_recipients()
address_id = 0

bookshelf_isbn = ['9787115454157']  # 流畅的python
bookshelf_book_info = {'name': 'test_name', 'spu_id': 'test_spu'}
bookshelf_total = 0

bookshelf_user_old_signature = ''
new_signature = get_random_recipients()  # new_signature = '' 空字符串，即可以运行出bug

book_list_info = {}  # 最后格式如 {0:{'id': 'list_id', 'book_list_title': 'title'}, 1: ... }

book_group_info = {}  # 最后格式如 {0:{'id': 'group_id', 'book_group_title': 'title'}, 1: ... }

book_group_add_attention_ids = []
test_book_group_id = 0


def send_requests(method, url, params=None, json=None, headers=None, **kwargs):
    test_session = HttpRequests()
    response = test_session.send_request(method, url, params=params, json=json, headers=headers, **kwargs)
    test_session.close_session()
    return response


class TestAddAddress:
    """
    测试新增地址功能
    新增成功后，地址列表长度+1，地址列表最后一项为新增地址
    """

    @pytest.mark.run(order=1)
    def test_get_address_list(self):
        """
        获取用户地址列表
        """
        global address_total
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        address_total = r_json['data']['total']
        # print(self.address_total)

    @pytest.mark.run(order=2)
    def test_add_address(self):
        """
        添加地址
        """
        api = api_info[13]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['recipients'] = address_recipients
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    @pytest.mark.run(order=3)
    def test_get_address_new_list(self):
        """
        获取用户地址列表
        """
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['total'] == address_total+1
        assert r_json['data']['list'][-1]['recipients'] == address_recipients


class TestModifyAddress:
    """
    测试修改地址功能
    修改成功后，原地址相应信息发生改变；地址列表长度不变
    """

    @pytest.mark.run(order=1)
    def test_get_address_list(self):
        """
        获取用户地址列表
        """
        global address_id
        global address_total
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        address_id = r_json['data']['list'][1]['id']
        address_total = r_json['data']['total']

    @pytest.mark.run(order=2)
    def test_modify_address(self):
        """
        修改地址
        """
        api = api_info[14]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['recipients'] = address_recipients
        api['api_body']['id'] = address_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    @pytest.mark.run(order=3)
    def test_get_modify_result(self):
        """
        验证修改后地址是否与提交内容一致
        """
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        for address in r_json['data']['list']:
            if address['id'] == address_id:
                assert address['recipients'] == address_recipients
        assert r_json['data']['total'] == address_total


class TestBookshelfAddAndDeleteFavorite:
    """
    测试在个人书架-我的收藏中添加/删除图书
    添加成功后，我的收藏列表新增对应图书；删除成功后，我的收藏列表减少对应图书
    添加时，若书籍已存在我的收藏列表中，则code为720897，msg为"该书籍已在书架中"
    """

    @pytest.mark.run(order=1)
    def test_get_bookshelf_favorite_list(self):
        """
        获取我的藏书列表
        """
        global bookshelf_total
        api = api_info[28]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        bookshelf_total = r_json['data']['total']

    @pytest.mark.run(order=2)
    def test_query_book_spu_id(self):
        """
        通过isbn获取spu_id
        """
        global bookshelf_book_info
        api = api_info[35]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_params']['scan_value'] = bookshelf_isbn[0]
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        bookshelf_book_info['name'] = r_json['data']['items'][0]['name']
        bookshelf_book_info['spu_id'] = r_json['data']['items'][0]['spu_id']

    @pytest.mark.run(order=3)
    def test_bookshelf_add_favorite(self):
        """
        在个人书架-我的藏书添加图书（添加成功）
        """
        api = api_info[36]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['spu_id'] = bookshelf_book_info['spu_id']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    @pytest.mark.run(order=4)
    def test_is_add_success(self):
        """
        获取我的藏书列表，第一位是否为新添加的书 且 藏书总数是否+1
        """
        api = api_info[28]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['total'] == bookshelf_total + 1
        assert r_json['data']['items'][0]['id'] == bookshelf_book_info['spu_id']
        assert r_json['data']['items'][0]['title'] == bookshelf_book_info['name']

    @pytest.mark.run(order=5)
    def test_bookshelf_add_same_favorite(self):
        """
        在个人书架-我的藏书添加图书（重复添加）
        """
        api = api_info[36]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['spu_id'] = bookshelf_book_info['spu_id']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 720897
        assert r_json['msg'] == '该书籍已在书架中'

    @pytest.mark.run(order=6)
    def test_bookshelf_delete_favorites(self):
        """
        删除指定spu_id对应的记录
        """
        api = api_info[39]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['spu_ids'][0] = bookshelf_book_info['spu_id']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    @pytest.mark.run(order=7)
    def test_is_delete_success(self):
        """
        获取我的藏书列表，列表中无对应书籍 且 藏书总数是否与第一次获取列表时不发生变化
        """
        api = api_info[28]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['total'] == bookshelf_total
        for item in r_json['data']['items']:
            assert item['id'] != bookshelf_book_info['spu_id']
            assert item['title'] != bookshelf_book_info['name']


class TestModifyBookshelfUserProfileSignature:
    """
    测试个人书架页修改个人简介
    修改成功，再次获取个人书架-个人信息时，获取到的signature应该是修改内容
    修改内容为空字符串时，接口报修改成功，实际未修改数据库中对应字段值
    """

    @pytest.mark.run(order=1)
    def test_get_user_profilelite(self):
        """
        获取个人书架，我的个人信息
        """
        global bookshelf_user_old_signature
        api = api_info[27]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        bookshelf_user_old_signature += r_json['data']['signature']

    @pytest.mark.run(order=2)
    def test_modify_bookshelf_user_signature(self):
        """
        修改个人简介
        """
        api = api_info[38]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['signature'] = new_signature
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    @pytest.mark.run(order=3)
    def test_modified_signature_is_correct(self):
        """
        校验新获取的用户信息signature是否与修改内容一致
        """
        api = api_info[27]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['signature'] != bookshelf_user_old_signature or r_json['data']['signature'] == new_signature


class TestGetBooksAndConfigurationOfEveryBookList:
    """
    测试获取每个书单中的图书以及书单配置
    """

    @pytest.mark.run(order=1)
    def test_get_all_book_list_ids(self):
        """
        获取全部书单列表
        """
        global book_list_info
        api = api_info[17]
        # 获取全部普通书单id与书单title
        api['api_headers']['Authorization'] = tokens['token']
        r1 = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r1.status_code == 200
        r1_json = json.loads(r1.text)
        assert r1_json['code'] == 0
        for i in range(len(r1_json['data']['items'])):
            book_list_info[i] = {'id': r1_json['data']['items'][i]['id'], 'book_list_title': r1_json['data']['items'][i]['title']}
        # print(book_list_info)

        # 获取全部活动书单id与书单title
        api['api_params']['type'] = 1
        r2 = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r2.status_code == 200
        r2_json = json.loads(r2.text)
        assert r2_json['code'] == 0
        for i in range(len(r2_json['data']['items'])):
            book_list_info[i + len(r1_json['data']['items'])] = {'id': r2_json['data']['items'][i]['id'], 'book_list_title': r2_json['data']['items'][i]['title']}
        # print(book_list_info)

    @pytest.mark.run(order=2)
    def test_get_books_of_book_list(self):
        """
        测试能否获取每个书单的书籍列表（书单中书籍数量应>0）
        """
        api = api_info[26]
        api['api_headers']['Authorization'] = tokens['token']
        for i in range(book_list_info.__len__()):
            api['api_params']['id'] = book_list_info[i]['id']
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            # print('book list id is: ' + str(book_list_info[i]['id']))
            assert r.status_code == 200
            r_json = json.loads(r.text)
            assert r_json['code'] == 0
            if api['api_params']['id'] not in (57, 55):  # 这两个书单未设置内容
                assert r_json['data']['total'] > 0

    @pytest.mark.run(order=3)
    def test_get_configuration_of_book_list(self):
        """
        测试是否能获取每个书单的配置
        """
        api = api_info[23]
        api['api_headers']['Authorization'] = tokens['token']
        for i in range(book_list_info.__len__()):
            api['api_params']['id'] = book_list_info[i]['id']
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            # print('book list id is: ' + str(book_list_info[i]['id']))
            assert r.status_code == 200
            r_json = json.loads(r.text)
            # print(r_json)
            assert r_json['code'] == 0
            assert r_json['data']['title'] == book_list_info[i]['book_list_title']


class TestGetBooksOfEveryBookGroup:
    """
    测试获取每个分类中的图书
    """

    @pytest.mark.run(order=1)
    def test_get_all_book_group_ids(self):
        """
        获取全部分类id
        """
        global book_group_info
        flag = 1
        api = api_info[19]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        for i in range(len(r_json['data']['groups'])):
            book_group_info[i] = {'id': r_json['data']['groups'][i]['id'], 'name': r_json['data']['groups'][i]['name'], 'selected': r_json['data']['groups'][i]['selected']}
            if book_group_info[i]['selected'] is False:  # 用来判断是否有已选中的分类，用户必须选有分类
                flag = flag * 1
            else:
                flag = flag * 0
        assert flag == 0
        # print(book_group_info)

    @pytest.mark.run(order=2)
    def test_get_books_of_book_group(self):
        """
        获取每个分类下的图书
        """
        api = api_info[22]
        api['api_headers']['Authorization'] = tokens['token']
        for i in range(book_group_info.__len__()):
            api['api_params']['group_id'] = book_group_info[i]['id']
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            # print('book group id is: ' + str(book_group_info[i]['id']))
            assert r.status_code == 200
            r_json = json.loads(r.text)
            assert r_json['code'] == 0
            assert r_json['message'] == 'OK'
            assert r_json['data']['total'] > 0  # 分类下的图书列表，书籍数量应该>0


class TestAddAndDeleteAttentionOfBookGroup:
    """
    测试对分类添加关注和取消关注
    """

    @pytest.mark.run(order=1)
    def test_get_all_book_group_ids(self):
        """
        获取全部分类信息，主要是分类id、分类名、是否关注标志
        """
        global book_group_add_attention_ids
        global test_book_group_id
        api = api_info[19]
        api['api_headers']['Authorization'] = tokens['Bearer_token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        for i in range(len(r_json['data']['groups'])):
            if r_json['data']['groups'][i]['selected'] is True:  # 用来判断是否有已选中的分类，用户必须选有分类（取消完所有分类时，自动使用默认推荐分类）
                book_group_add_attention_ids.append(r_json['data']['groups'][i]['id'])
        # print(book_group_add_attention_ids)
        test_book_group_id = book_group_add_attention_ids[random.randint(0, len(book_group_add_attention_ids))]
        # print(test_book_group_id)

    @pytest.mark.run(order=2)
    def test_delete_attention_of_book_group(self):
        """
        对一个已关注分类取消关注
        """
        api = api_info[72]
        api['api_headers']['Authorization'] = tokens['Bearer_token']
        api['api_body']['id'] = test_book_group_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['message'] == 'OK'

    @pytest.mark.run(order=3)
    def test_delete_attention_is_success(self):
        """
        获取全部分类信息，查看已取消关注的分类的是否关注标志为false
        """
        api = api_info[19]
        api['api_headers']['Authorization'] = tokens['Bearer_token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        # print(r_json)
        for i in range(len(r_json['data']['groups'])):
            if r_json['data']['groups'][i]['id'] == test_book_group_id:
                assert r_json['data']['groups'][i]['selected'] is False

    @pytest.mark.run(order=4)
    def test_add_attention_of_book_group(self):
        """
        对已取消关注的分类添加关注
        """
        api = api_info[72]
        api['api_headers']['Authorization'] = tokens['Bearer_token']
        api['api_body']['id'] = test_book_group_id
        api['api_body']['action'] = '1'
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['message'] == 'OK'

    @pytest.mark.run(order=5)
    def test_add_attention_is_success(self):
        """
        获取全部分类信息，查看添加关注的分类的是否关注标志为true
        """
        api = api_info[19]
        api['api_headers']['Authorization'] = tokens['Bearer_token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        for i in range(len(r_json['data']['groups'])):
            if r_json['data']['groups'][i]['id'] == test_book_group_id:
                assert r_json['data']['groups'][i]['selected'] is True
