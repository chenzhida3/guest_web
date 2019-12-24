# -*- coding: utf-8 -*-
'''
 @File    : views_if_sec.py
 @Time    : 2019/6/25 8:35
 @Author  : Chenzd
 @Project : 接口安全
 @Software: PyCharm
'''
import base64

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import auth as django_auth

from sign.models import Event


def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('iso-8859-1').partition(':')
    except IndexError:
        return 'null'

    userid, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=userid, password=password)
    if user is not None and user.is_active:
        django_auth.login(request, user)
        return "success"
    else:
        return "fail"

def get_event_list(request):
    '''发布会查询接口--增加用户认证'''
    user_result = user_auth(request)
    if user_result == 'null':
        return JsonResponse({'status': 10011, 'message': 'user auth null'})
    if user_result == 'fail':
        return JsonResponse({'status': 10012, 'message': 'user auth fail'})
    eid = request.GET.get('eid', '')  # 发布会id
    name = request.GET.get('name', '')  # 发布会名称
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist as e:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['satrt_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        datas = []
        result = Event.objects.filter(name__contains=name)
        if result:
            for i in result:
                event = {}
                event['name'] = i.name
                event['limit'] = i.limit
                event['status'] = i.status
                event['address'] = i.address
                event['satrt_time'] = i.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
