# -*- coding: utf-8 -*-
# @Author: MirrorAi
# @Date:   2020/2/16 17:21

# import pytest
import json
import random
from api_information import api_info, tokens, main_url
from test_get_apis import HttpRequests
from tools import get_random_recipients, str_to_timestamp


add_new_address_total = 0
modify_address_total = 0
address_recipients = get_random_recipients()
new_address_recipients = get_random_recipients()
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

recycle_cart_isbn = ['9787115454157', '9787544270878', '9787544242516', '9787546302393', '9787544241694', '9787532725694']
recycle_cart_book_info = {}  # 最后格式如 {'isbn':{'spu_id': 'spu_id', 'name': 'name', 'original_price': 'original_price', 'id': 'recycle_cart_id'}, 'isbn2': ... }
recycle_cart_book_num = 0

create_recycle_order_cart_book_info = {}
create_recycle_order_cart_num = 0
old_address_id = 0
old_address_detail = {}
new_address_id = 0
new_address_detail = {}
old_pickup_time = {}
new_pickup_time = {}
recycle_order_id = ''

sell_cart_spu_ids = ['9632856317100035', '9632989018587137', '9633052173008896', '9632558189117440', '9634357812396038']  # 岛上书店，好吗好的，乖摸摸头，我不，你坏
sell_cart_sku_ids = {}  # {spu:sku, spu2:sku2, ...}
sell_cart_book_info = {}  # {'spu':{'sku':'sku', 'id':'id', 'select':'select_flag', 'stocks':stock_num}, 'spu2':...}
sell_cart_total = 0


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

    # @pytest.mark.run(order=1)
    def test_get_address_list(self):
        """
        获取用户地址列表
        """
        global add_new_address_total
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        add_new_address_total = r_json['data']['total']
        # print(self.address_total)

    # @pytest.mark.run(order=1)
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

    # @pytest.mark.run(order=1)
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
        assert r_json['data']['total'] == add_new_address_total + 1
        assert r_json['data']['list'][-1]['recipients'] == address_recipients


class TestModifyAddress:
    """
    测试修改地址功能
    修改成功后，原地址相应信息发生改变；地址列表长度不变
    """

    # @pytest.mark.run(order=1)
    def test_get_address_list(self):
        """
        获取用户地址列表
        """
        global address_id
        global modify_address_total
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        address_id = r_json['data']['list'][1]['id']
        modify_address_total = r_json['data']['total']
        # print(r_json)

    # @pytest.mark.run(order=2)
    def test_modify_address(self):
        """
        修改地址
        """
        api = api_info[14]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['recipients'] = new_address_recipients
        api['api_body']['id'] = address_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    # @pytest.mark.run(order=3)
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
                assert address['recipients'] == new_address_recipients
        # print(r_json)
        assert r_json['data']['total'] == modify_address_total #????


class TestBookshelfAddAndDeleteFavorite:
    """
    测试在个人书架-我的收藏中添加/删除图书
    添加成功后，我的收藏列表新增对应图书；删除成功后，我的收藏列表减少对应图书
    添加时，若书籍已存在我的收藏列表中，则code为720897，msg为"该书籍已在书架中"
    """

    # @pytest.mark.run(order=1)
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

    # @pytest.mark.run(order=2)
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

    # @pytest.mark.run(order=3)
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

    # @pytest.mark.run(order=4)
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

    # @pytest.mark.run(order=5)
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

    # @pytest.mark.run(order=6)
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

    # @pytest.mark.run(order=7)
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

    # @pytest.mark.run(order=1)
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

    # @pytest.mark.run(order=2)
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

    # @pytest.mark.run(order=3)
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

    # @pytest.mark.run(order=1)
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

    # @pytest.mark.run(order=2)
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

    # @pytest.mark.run(order=3)
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

    # @pytest.mark.run(order=1)
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

    # @pytest.mark.run(order=2)
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

    # @pytest.mark.run(order=1)
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
        test_book_group_id = book_group_add_attention_ids[random.randint(0, len(book_group_add_attention_ids) - 1)]
        # print(test_book_group_id)

    # @pytest.mark.run(order=2)
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

    # @pytest.mark.run(order=3)
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

    # @pytest.mark.run(order=4)
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

    # @pytest.mark.run(order=5)
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


class TestAddAndDeleteBookToRecycleCart:
    """
    测试添加/删除书籍到回收车
    """

    # @pytest.mark.run(order=1)
    def test_get_recycle_cart_books(self):
        """
        获取回收车中书籍
        """
        global recycle_cart_book_num
        api = api_info[46]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        recycle_cart_book_num = r_json['data']['quantity']

    # @pytest.mark.run(order=2)
    def test_get_book_spu_id(self):
        """
        通过书籍isbn获取spu_id
        """
        global recycle_cart_book_info
        api = api_info[47]
        api['api_headers']['Authorization'] = tokens['token']
        for isbn in recycle_cart_isbn:
            api['api_params']['scan_value'] = isbn
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            assert r.status_code == 200
            r_json = json.loads(r.text)
            assert r_json['code'] == 0
            recycle_cart_book_info[isbn] = {'spu_id': r_json['data']['items'][0]['spu_id'], 'name': r_json['data']['items'][0]['name'], 'original_price': r_json['data']['items'][0]['original_price']}
        # print(recycle_cart_book_info)

    # @pytest.mark.run(order=3)
    def test_add_book_to_recycle_cart(self):
        """
        添加书籍到回收车
        """
        global recycle_cart_book_num
        api = api_info[48]
        api['api_headers']['Authorization'] = tokens['token']
        for isbn in recycle_cart_isbn:
            api['api_body']['spu_id'] = recycle_cart_book_info[isbn]['spu_id']
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            assert r.status_code == 200
            r_json = json.loads(r.text)
            # print(api['api_body'])
            # print(r_json)
            assert r_json['code'] == 0
            recycle_cart_book_num += 1

    # @pytest.mark.run(order=4)
    def test_is_add_success(self):
        """
        校验是否添加成功（添加前回收车中书籍数量为0）
        """
        global recycle_cart_book_info
        api = api_info[46]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert recycle_cart_book_num == r_json['data']['quantity']  # 断言添加成功后total数量有没有相应增加
        for i in range(len(r_json['data']['items'])):  # 拿获取的回收车书籍列表与添加图书的列表对比是否一致
            spu_id = r_json['data']['items'][i]['spu_id']
            name = r_json['data']['items'][i]['name']
            original_price = r_json['data']['items'][i]['original_price']
            for isbn in recycle_cart_isbn:
                if recycle_cart_book_info[isbn]['spu_id'] == spu_id:
                    assert name == recycle_cart_book_info[isbn]['name']
                    assert original_price == recycle_cart_book_info[isbn]['original_price']
                    recycle_cart_book_info[isbn]['id'] = str(r_json['data']['items'][i]['id'])
        # print(recycle_cart_book_info)

    # @pytest.mark.run(order=5)
    def test_delete_book_in_recycle_cart(self):
        """
        在回收车删除书籍
        """
        global recycle_cart_book_num
        api = api_info[77]
        api['api_headers']['Authorization'] = tokens['token']
        for isbn in recycle_cart_isbn:
            api['api_body']['id'] = recycle_cart_book_info[isbn]['id']
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            assert r.status_code == 200
            r_json = json.loads(r.text)
            assert r_json['code'] == 0
            recycle_cart_book_num -= 1

    # @pytest.mark.run(order=6)
    def test_is_delete_success(self):
        """
        校验是否删除成功
        """
        flag = 0
        api = api_info[46]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert recycle_cart_book_num == r_json['data']['quantity']
        if recycle_cart_book_num == 0:
            assert len(r_json['data']['items']) == 0
        else:
            for i in range(len(r_json['data']['items'])):  # 拿获取的回收车书籍列表与添加图书的列表对比，是否没删除掉
                isbn = r_json['data']['items'][i]['description_units'][0]['value']
                try:
                    print(recycle_cart_book_info[isbn])  # 如果响应中还能找到对应isbn
                except KeyError:
                    flag = 0
                else:
                    flag = 1
                finally:
                    assert flag == 0


class TestRecycleOrder:
    """
    测试生成回收订单、修改回收订单收货地址、修改回收订单取件时间、取消回收订单流程
    生成回收订单时，需要选择有效地址、取件时间，将回收车内的所有书创建为一个回收单
    生成成功后，该回收订单的详情信息应与回收车中书籍详情一致
    """

    # @pytest.mark.run(order=1)
    def test_get_recycle_cart_books(self):
        """
        获取回收车中书籍
        """
        global create_recycle_order_cart_num
        api = api_info[46]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        create_recycle_order_cart_num = r_json['data']['quantity']

    # @pytest.mark.run(order=2)
    def test_get_book_spu_id(self):
        """
        通过书籍isbn获取spu_id
        """
        global create_recycle_order_cart_book_info
        api = api_info[47]
        api['api_headers']['Authorization'] = tokens['token']
        for isbn in recycle_cart_isbn:
            api['api_params']['scan_value'] = isbn
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            assert r.status_code == 200
            r_json = json.loads(r.text)
            assert r_json['code'] == 0
            create_recycle_order_cart_book_info[isbn] = {'spu_id': r_json['data']['items'][0]['spu_id'], 'name': r_json['data']['items'][0]['name'], 'original_price': r_json['data']['items'][0]['original_price']}
        # print(create_recycle_cart_book_info)

    # @pytest.mark.run(order=3)
    def test_add_book_to_recycle_cart(self):
        """
        添加书籍到回收车
        """
        global create_recycle_order_cart_num
        api = api_info[48]
        api['api_headers']['Authorization'] = tokens['token']
        print(recycle_cart_isbn)
        print(create_recycle_order_cart_book_info)
        for isbn in recycle_cart_isbn:
            api['api_body']['spu_id'] = create_recycle_order_cart_book_info[isbn]['spu_id']
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            assert r.status_code == 200
            r_json = json.loads(r.text)
            print(r_json)
            print(isbn)
            print(api['api_body'])
            assert r_json['code'] == 0 #???
            create_recycle_order_cart_num += 1
        print(create_recycle_order_cart_num)

    # @pytest.mark.run(order=4)
    def test_get_address_id(self):
        """
        获取用户收货地址
        """
        global old_address_id, old_address_detail
        global new_address_id, new_address_detail
        api = api_info[12]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        old_address = r_json['data']['list'][random.randint(0, r_json['data']['total'] - 1)]
        old_address_id = old_address['id']
        old_address_detail['sender_name'] = old_address['recipients']
        old_address_detail['sender_tel'] = old_address['tel']
        old_address_detail['address_town'] = old_address['town']
        old_address_detail['address_detailed'] = old_address['detail']
        new_address = r_json['data']['list'][random.randint(0, r_json['data']['total'] - 1)]
        while new_address == old_address:
            new_address = r_json['data']['list'][random.randint(0, r_json['data']['total'] - 1)]
        new_address_id = new_address['id']
        new_address_detail['sender_name'] = new_address['recipients']
        new_address_detail['sender_tel'] = new_address['tel']
        new_address_detail['address_town'] = new_address['town']
        new_address_detail['address_detailed'] = new_address['detail']

    # @pytest.mark.run(order=5)
    def test_get_pickup_time(self):
        """
        获取当前时间可选取件时间
        """
        global old_pickup_time
        global new_pickup_time
        api = api_info[45]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        old_num = random.randint(0, len(r_json['data']) - 1)
        new_num = random.randint(0, len(r_json['data']) - 1)
        while new_num == old_num:
            new_num = random.randint(0, len(r_json['data']) - 1)
        # print(r_json['data'][old_num]['date'][:10])
        # print(r_json['data'][new_num]['date'][:10])
        # print(r_json['data'][old_num]['periods'][0])
        # print(r_json['data'][new_num]['periods'][0])
        old_pickup_time = {'date': r_json['data'][old_num]['date'][:10], 'period': r_json['data'][old_num]['periods'][0]}
        new_pickup_time = {'date': r_json['data'][new_num]['date'][:10], 'period': r_json['data'][new_num]['periods'][0]}

    # @pytest.mark.run(order=6)
    def test_create_recycle_order(self):
        """
        生成回收订单
        """
        global recycle_order_id
        api = api_info[43]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['address_id'] = old_address_id
        api['api_body']['pick_up_date'] = old_pickup_time['date']
        api['api_body']['pick_up_period'] = old_pickup_time['period']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        # print(api['api_body'])
        # print(r_json)
        assert r_json['code'] == 0
        recycle_order_id = r_json['data']['id']

    # @pytest.mark.run(order=7)
    def test_recycle_order_detail_is_correct(self):
        """
        获取回收订单详情，看书籍信息是否匹配、订单状态是否为待确认0
        """
        api = api_info[42]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_params']['id'] = recycle_order_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['order']['status'] == 0
        assert r_json['data']['address']['address_town'] == old_address_detail['address_town']
        assert r_json['data']['address']['address_detailed'] == old_address_detail['address_detailed']
        assert r_json['data']['address']['sender_name'] == old_address_detail['sender_name']
        assert r_json['data']['address']['sender_tel'] == old_address_detail['sender_tel']
        assert r_json['data']['address']['pickup_start_time'] == str_to_timestamp(old_pickup_time['date'] + ' ' + old_pickup_time['period'].split('-')[0] + ':00')
        assert r_json['data']['address']['pickup_end_time'] == str_to_timestamp(old_pickup_time['date'] + ' ' + old_pickup_time['period'].split('-')[-1] + ':00')

    # @pytest.mark.run(order=8)
    def test_modify_address(self):
        """
        修改地址
        """
        api = api_info[50]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['recycle_order_id'] = recycle_order_id
        api['api_body']['address_id'] = new_address_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    # @pytest.mark.run(order=9)
    def test_modify_address_is_success(self):
        """
        获取回收订单详情，看地址是否发生改变
        """
        api = api_info[42]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_params']['id'] = recycle_order_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['order']['status'] == 0
        assert r_json['data']['address']['address_town'] == new_address_detail['address_town']
        assert r_json['data']['address']['address_detailed'] == new_address_detail['address_detailed']
        assert r_json['data']['address']['sender_name'] == new_address_detail['sender_name']
        assert r_json['data']['address']['sender_tel'] == new_address_detail['sender_tel']
        assert r_json['data']['address']['pickup_start_time'] == str_to_timestamp(old_pickup_time['date'] + ' ' + old_pickup_time['period'].split('-')[0] + ':00')
        assert r_json['data']['address']['pickup_end_time'] == str_to_timestamp(old_pickup_time['date'] + ' ' + old_pickup_time['period'].split('-')[-1] + ':00')

    # @pytest.mark.run(order=10)
    def test_modify_pickup_time(self):
        """
        修改取件时间
        """
        api = api_info[51]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['recycle_order_id'] = recycle_order_id
        api['api_body']['pick_up_date'] = new_pickup_time['date']
        api['api_body']['pick_up_period'] = new_pickup_time['period']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    # @pytest.mark.run(order=11)
    def test_modify_pickup_time_is_success(self):
        """
        获取回收订单详情，看取件时间是否发生改变
        """
        api = api_info[42]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_params']['id'] = recycle_order_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['order']['status'] == 0
        assert r_json['data']['address']['address_town'] == new_address_detail['address_town']
        assert r_json['data']['address']['address_detailed'] == new_address_detail['address_detailed']
        assert r_json['data']['address']['sender_name'] == new_address_detail['sender_name']
        assert r_json['data']['address']['sender_tel'] == new_address_detail['sender_tel']
        assert r_json['data']['address']['pickup_start_time'] == str_to_timestamp(new_pickup_time['date'] + ' ' + new_pickup_time['period'].split('-')[0] + ':00')
        assert r_json['data']['address']['pickup_end_time'] == str_to_timestamp(new_pickup_time['date'] + ' ' + new_pickup_time['period'].split('-')[-1] + ':00')

    # @pytest.mark.run(order=12)
    def test_cancel_recycle_order(self):
        """
        取消回收订单
        """
        api = api_info[44]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['id'] = recycle_order_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0

    # @pytest.mark.run(order=13)
    def test_cancel_is_success(self):
        """
        获取回收订单详情，看订单状态是否发生改变（已取消回收订单状态为-1）
        """
        api = api_info[42]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_params']['id'] = recycle_order_id
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['order']['status'] == -1


class TestAddAndDeleteBookToSellCart:
    """
    测试在购物车中添加/删除图书
    """

    # @pytest.mark.run(order=1)
    def test_get_sell_cart_books(self):
        """
        获取购物车中图书，按库存数量分为有货、无货；按选中状态分为选中、未选中
        """
        global sell_cart_total
        api = api_info[55]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        sell_cart_total = r_json['data']['total']

    # @pytest.mark.run(order=2)
    def test_get_book_sku_id(self):
        """
        通过spu获取sku，sku用来加购物车
        """
        global sell_cart_sku_ids
        api = api_info[78]
        api['api_headers']['Authorization'] = tokens['token']
        for spu_id in sell_cart_spu_ids:
            api['api_params']['spu_id'] = spu_id
            r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
            assert r.status_code == 200
            r_json = json.loads(r.text)
            assert r_json['code'] == 0
            for item in r_json['data']['list']:
                # print(item)
                if item['stock_num'] > 0:  # 获取第一项有库存的书，其sku记在要加入购物车的sku中
                    sell_cart_sku_ids[spu_id] = item['sku_id']
                    break
        # print(sell_cart_sku_ids)

    # @pytest.mark.run(order=3)
    def test_add_book_to_sell_cart(self):
        """
        向购物车中添加图书
        """
        global sell_cart_total
        sku_ids = []
        for v in sell_cart_sku_ids.values():
            sku_ids.append(v)
        api = api_info[53]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['sku_ids'] = sku_ids
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        sell_cart_total += len(sku_ids)

    # @pytest.mark.run(order=4)
    def test_add_book_is_success(self):
        """
        获取购物车列表，看添加图书是否成功
        """
        global sell_cart_book_info
        api = api_info[55]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['total'] == sell_cart_total
        for k, v in sell_cart_sku_ids.items():
            flag = 0
            for good_info in r_json['data']['list']:
                if good_info['goods']['spu_id'] == k:  # 能在购物车列表中找到加入的商品，flag为1；找不到，则flag为0
                    assert good_info['goods']['sku_id'] == v
                    flag = 1
                    sell_cart_book_info[good_info['goods']['spu_id']] = {'sku': good_info['goods']['sku_id'],
                                                                         'id': good_info['id'],
                                                                         'select': good_info['select'],
                                                                         'stocks': good_info['stocks']}
            assert flag == 1

    # @pytest.mark.run(order=5)
    def test_delete_book_in_sell_cart(self):
        """
        在购物车中删除图书
        """
        global sell_cart_total
        ids = []
        for k in sell_cart_sku_ids.keys():
            ids.append(sell_cart_book_info[k]['id'])
        api = api_info[54]
        api['api_headers']['Authorization'] = tokens['token']
        api['api_body']['ids'] = ids
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'], api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        sell_cart_total -= len(ids)

    # @pytest.mark.run(order=6)
    def test_delete_book_is_success(self):
        """
        获取购物车列表，看删除图书是否成功
        """
        api = api_info[55]
        api['api_headers']['Authorization'] = tokens['token']
        r = send_requests(api['api_method'], main_url + api['api_url'], api['api_params'], api['api_body'],
                          api['api_headers'], verify=False)
        assert r.status_code == 200
        r_json = json.loads(r.text)
        assert r_json['code'] == 0
        assert r_json['data']['total'] == sell_cart_total
        for k, v in sell_cart_sku_ids.items():
            flag = 1
            for good_info in r_json['data']['list']:
                if good_info['goods']['spu_id'] == k:  # 能在购物车列表中找到加入的商品，flag为0；找不到，则flag为1
                    assert good_info['goods']['sku_id'] == v
                    flag = 0
            assert flag == 1
