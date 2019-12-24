from datetime import datetime

from django.test import TestCase
from sign.models import Event,Guest
from django.test import Client
from django.contrib.auth.models import User
# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="OPPO Reno新品发布会", status=True, limit=2000,
                             address='孙厝路口', start_time='2019-08-31 15:18:22')
        Guest.objects.create(id=1, event_id=1, realname='玛利亚',
                             phone='13711001101', email='maliya@mail.com', sign=False)
    def test_event_models(self):
        '''测试新建发布会'''
        result = Event.objects.get(name="OPPO Reno新品发布会")
        self.assertEqual(result.address, "孙厝路口", '结果：错误')
        self.assertTrue(result.status)

    def test_guest_models(self):
        '''测试邀请嘉宾'''
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "玛利亚")
        self.assertFalse(result.sign)

class loginActionTest(TestCase):
    '''测试登录模块'''
    def setUp(self):
        User.objects.create_user('chenzhida', 'chenzhida@mail.com', 'admin123456')
        self.c = Client()

    def test01_login(self):
        '''用户名和密码为空'''
        test_data= {'username': '', 'password': ''}
        respone = self.c.post('/login_action/', data=test_data)
        self.assertEqual(respone.status_code, 200, '结果：密码账号为空异常')
        self.assertIn(b"username or password error!", respone.content)

    def test02_login(self):
        '''用户名和密码为错误'''
        test_data= {'username': 'abc', 'password': '123456'}
        respone = self.c.post('/login_action/', data=test_data)
        self.assertEqual(respone.status_code, 200, '结果：密码账号为错误时异常')
        self.assertIn(b"username or password error!", respone.content)

    def test03_login(self):
        '''用户名错误和密码为正确'''
        test_data= {'username': 'dcasdc', 'password': 'admin123456'}
        respone = self.c.post('/login_action/', data=test_data)
        self.assertEqual(respone.status_code, 200, '结果：用户名控和密码为正确异常')
        self.assertIn(b"username or password error!", respone.content)

    def test04_login(self):
        '''用户名正确和密码为错误'''
        test_data= {'username': 'chenzhida', 'password': 'asbdfkasndf'}
        respone = self.c.post('/login_action/', data=test_data)
        self.assertEqual(respone.status_code, 200, '结果：用户名正确和密码为空异常')
        self.assertIn(b"username or password error!", respone.content)

    def test05_login(self):
        '''用户名正确和密码正确'''
        test_data= {'username': 'chenzhida', 'password': 'admin123456'}
        respone = self.c.post('/login_action/', data=test_data)
        self.assertEqual(respone.status_code, 302, '结果：用户名正确和密码为空异常')

class EventManageTest(TestCase):
    ''' 发布会管理'''

    def setUp(self):
        Event.objects.create(id=3, name="mate20",limit=2000,status=True,
                             address="beijing",start_time=datetime(2019, 6, 21, 14, 0, 0))
        self.c = Client()

    def test_event_manage_success(self):
        ''' 测试发布会:mate20 '''
        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"mate20", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_manage_search_success(self):
        ''' 测试发布会搜索'''
        response = self.c.post('/search_name/', {"name": "xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"mate20", response.content)
        self.assertIn(b"beijing", response.content)

class GuestManageTest(TestCase):
    ''' 嘉宾管理'''

    def setUp(self):
        Event.objects.create(id=3, name="mate20",limit=2000,status=True,
                             address="beijing",start_time=datetime(2019, 6, 21, 14, 0, 0))
        Guest.objects.create(id=1, event_id=3, realname='maliya',
                             phone='13711001101', email='maliya@mail.com', sign=False)
        self.c = Client()

    def test_event_manage_success(self):
        ''' 测试嘉宾信息:玛利亚 '''
        response = self.c.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"maliya", response.content)
        self.assertIn(b"13711001101", response.content)

    def test_event_manage_search_success(self):
        ''' 测试嘉宾搜索'''
        response = self.c.post('/search_guest/', {"name": "maliya"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"maliya", response.content)
        self.assertIn(b"13711001101", response.content)


class SignIndexActionTest(TestCase):
    ''' 发布会签到'''
    def setUp(self):
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address='beijing',
                             status=1,start_time='2019-6-22 12:30:00')
        Event.objects.create(id=2,name="oneplus4",limit=2000,address='shenzhen',
                             status=1,start_time='2019-6-22 12:30:00')
        Guest.objects.create(realname="alen",phone=18611001100,
                             email='alen@mail.com',sign=0,event_id=1)
        Guest.objects.create(realname="una",phone=18611001101,
                             email='una@mail.com',sign=1,event_id=2)
        self.c = Client()

    def test_phone_null(self):
        '''手机号为空'''
        respone = self.c.post('/sign_index_action/1/', {'phone': ''})
        self.assertEqual(respone.status_code, 200)
        self.assertIn(b'phone error',respone.content)

    def test_phone_error_for_event(self):
        '''手机号或发布会错误'''
        respone = self.c.post('/sign_index_action/2/', {'phone': '18611001100'})
        self.assertEqual(respone.status_code, 200)
        self.assertIn(b"event id or phone error.", respone.content)

    def test_sign_has(self):
        '''用户已签到'''
        respone = self.c.post('/sign_index_action/2/', {'phone': '18611001101'})
        self.assertEqual(respone.status_code, 200)
        self.assertIn(b"user has sign in.", respone.content)

    def test_sign_success(self):
        '''用户签到成功'''
        respone = self.c.post('/sign_index_action/1/', {'phone': '18611001100'})
        self.assertEqual(respone.status_code, 200)
        self.assertIn(b"sign in success!", respone.content)